import execjs
import requests
import py_moss_helper
import json
import os
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
import codecs

jscode = open("1.js", "r", encoding="utf-8").read()
exec_js = execjs.compile(jscode)
gpage={}
#chrome.exe --remote-debugging-port=8899 --user-data-dir="userdata"
#"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=8899 --user-data-dir="userdata"

question_urls=[] #问题帖子集合
p_urls=[] #专栏文章集合
datas_pagedata = []

def scroll_to_bottom(page):
    page.evaluate("""() => {
        return  new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 600;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 200);
        })
    }""")


class ZhiHu:
    def __init__(self):
        self.helper = py_moss_helper.Helper()
        self.page = {}

        self.pagedata={}
        self.pagedata['answers_objs'] = []
        self.pagedata['url'] = ""
        self.pagedata['answers_id'] = ""
        self.pagedata['title'] = ""
        self.pagedata['question_text'] = ""
        self.pagejson={}

    def getpage(self,url, context):
        self.page = context.new_page()

        self.pagedata['url'] = url  # 获取问题链接
        self.pagedata['answers_id'] = url.split('/')[-1]

        a= self.page.goto(url)
        self.pagejson =json.loads(str(self.getpage_json(a.text(),context)[0]))

        self.pagedata['title'] = self.page.query_selector('h1').inner_text()  # 获取问题标题
        question_text_html = self.pagejson['initialState']['entities']['questions'][self.pagedata['answers_id']]['detail']  # 获取问题正文
        # 提取纯文本
        self.pagedata['question_text']=BeautifulSoup(question_text_html, 'lxml').get_text(separator=' ', strip=True)
        #self.page.add_script_tag(path="./pagejs.js")
        self.getpage_answers() #获取回答



        datas_pagedata.append(self.pagedata)
        print(json.dumps(self.pagedata, ensure_ascii=False))


    def getpage_json(self,htmltext, context):
        script_content = py_moss_helper.Helper.getXpath(htmltext,"//script[@id='js-initialData']/text()")
        if not script_content:
            raise "文字内同脚本为空"
        return script_content
    def getpage_answers(self):
        answersjson = self.pagejson['initialState']['entities']['answers']
        for answer_id, answer_data in answersjson.items():
            answer={}
            answer['pl_objs']=[] #回答评论集合
            answer['id']=answer_id #回答id
            answer['text'] = BeautifulSoup(answer_data['content'], 'lxml').get_text(separator=' ',strip=True) #回答正文
            self.pagedata['answers_objs'].append(answer)
            print(answer)

        next_answer_url = self.pagejson['initialState']['question']['answers'][self.pagedata['answers_id']]['next']
        self.getpage_next_answers(next_answer_url)
    def getpage_next_answers(self,next_answer_url):
        next_answer_json= self.page.request.get(next_answer_url).json()
        if len(next_answer_json['data'])==0:
            return
        for answeritem in next_answer_json['data']:
            answer={}
            answer['pl_objs'] = []
            answer['id']=answeritem['target']['id']
            answer['text'] = BeautifulSoup(answeritem['target']['content'], 'lxml').get_text(separator=' ',strip=True)
            self.pagedata['answers_objs'].append(answer)
            print(answer)
        self.getpage_next_answers(next_answer_json['paging']['next'])

    def goto_pl_url(self,pl_url,answer):
        cookies = self.page.context.cookies('https://www.zhihu.com')
        cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
        # 调js
        zse96_md5 = exec_js.call('justmd5', pl_url, cookie_string)
        # 执行注入的 JavaScript 文件中的函数，并传递参数
        zse96 = "2.0" + "_" + gpage.evaluate(f"window.myFunction('{zse96_md5}')")
        headers = {
            'x-zse-93': '101_3_3.0',
            'x-zse-96': zse96,
            'cookie': cookie_string
        }
        res = self.page.request.get(pl_url,headers=headers)
        pl_json = res.json()['data']
        if len(pl_json)==0:
            return
        for plitem in pl_json:
            plobj={}
            plobj['pl_text'] = BeautifulSoup(plitem['content'], 'lxml').get_text(separator=' ',strip=True)
            answer['pl_objs'].append(plobj)
            print(plobj)
        self.goto_pl_url(res.json()['paging']['next'],answer)

def getpage_task(url, context):
    zhihu = ZhiHu()
    zhihu.getpage(url, context)
    # 爬评论
    for answer in zhihu.pagedata['answers_objs']:
        pl_url = f"https://www.zhihu.com/api/v4/comment_v5/answers/{answer['id']}/root_comment?order_by=score&limit=20&offset="
        zhihu.goto_pl_url(pl_url,answer) #调逆向评论
        print("当前回答评论采集结束",answer['id'])

    zhihu.page.close()
if __name__ == '__main__':
    # 打开并读取HTML文件
    with codecs.open('1.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 解析HTML内容
    html_tree = etree.HTML(html_content)
    # 提取类名为"content"的div元素内的文本
    content_divs = html_tree.xpath('//a[@data-za-detail-view-id="3942"]/@href')

    for content in content_divs:
        if content.startswith("//zhuanlan.zhihu.com"):
            content = "https:"+content
            if content not in p_urls:
                p_urls.append(content)
        elif content.startswith("/question"):
            content = "https://www.zhihu.com"+content
        answer_index = content.find('answer')
        if answer_index != -1:
            content= content[:answer_index-1]
            if content not in question_urls:
                question_urls.append(content)
    print(question_urls,p_urls)

    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp('http://localhost:8899/')
        # context = browser.contexts[0]
        browser = playwright.chromium
        context = browser.launch_persistent_context(
            user_data_dir='userdata',
            accept_downloads=True,
            headless=False,
            bypass_csp = True
        )
        context.add_init_script(path='./stealth.min.js')
        #登录
        gpage = context.new_page()
        gpage.goto("https://www.zhihu.com")
        # 假设登录成功后页面上会出现用户名元素，例如一个id为'username'的标签
        dengdai=True
        while dengdai:
            gpage.wait_for_load_state('networkidle')
            login_button = gpage.query_selector_all('button:text("登录/注册")')
            if login_button:
                print("尚未登录")
                gpage.wait_for_timeout(1000)
            else:
                print("已登录或元素不存在")
                dengdai=False
        print("登录成功")
        gpage.add_script_tag(path="./pagejs.js")
        #ckobj = page.goto("https://www.zhihu.com/search?type=content&q=%E6%8B%9B%E6%8A%95%E6%A0%87%E5%9B%A0%E4%B8%BAip%E7%9B%B8%E5%90%8C%E8%A2%AB%E5%A4%84%E7%BD%9A")
        #---------------------------

        for url in question_urls:
            getpage_task(url, context)
        # ---------------------
        context.close()


