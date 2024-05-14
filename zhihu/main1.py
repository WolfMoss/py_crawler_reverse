import execjs

import py_moss_helper
import json
import os
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
import codecs
#chrome.exe --remote-debugging-port=8899 --user-data-dir="userdata"
#"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=8899 --user-data-dir="userdata"


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

question_urls=[] #问题帖子集合
p_urls=[] #专栏文章集合
datas_pagedata = []
jscode = open("1.js", "r", encoding="utf-8").read()

class ZhiHu:
    def __init__(self):
        self.helper = py_moss_helper.Helper()
        self.page = context.new_page()

        self.pagedata={}
        self.pagedata['answers_objs'] = []
        self.pagedata['url'] = ""
        self.pagedata['answers_id'] = ""
        self.pagedata['title'] = ""
        self.pagedata['question_text'] = ""
        self.pagejson={}

    def getpage(self,url, context):
        self.pagedata['url'] = url  # 获取问题链接
        self.pagedata['answers_id'] = url.split('/')[-1]

        a= self.page.goto(url)
        self.pagejson =json.loads(str(self.getpage_json(a.text(),context)[0]))

        self.pagedata['title'] = self.page.query_selector('h1').inner_text()  # 获取问题标题
        question_text_html = self.pagejson['initialState']['entities']['questions'][self.pagedata['answers_id']]['detail']  # 获取问题正文
        # 提取纯文本
        self.pagedata['question_text']=BeautifulSoup(question_text_html, 'lxml').get_text(separator=' ', strip=True)

        self.getpage_answers() #获取回答



        datas_pagedata.append(self.pagedata)
        print(json.dumps(self.pagedata, ensure_ascii=False))
        self.page.close()

    def getpage_json(self,htmltext, context):
        script_content = py_moss_helper.Helper.getXpath(htmltext,"//script[@id='js-initialData']/text()")
        if not script_content:
            raise "文字内同脚本为空"
        return script_content
    def getpage_answers(self):
        answersjson = self.pagejson['initialState']['entities']['answers']
        for answer_id, answer_data in answersjson.items():
            answer={}
            answer['id']=answer_id
            answer['text'] = BeautifulSoup(answer_data['content'], 'lxml').get_text(separator=' ',strip=True)
            self.pagedata['answers_objs'].append(answer)

            #测试
            pl_url = f"https://www.zhihu.com/api/v4/comment_v5/answers/{answer_id}/root_comment?order_by=score&limit=20&offset="
            doccookie = self.page.evaluate("""() => {
                return document.cookie
            }""")
            # 调js
            #读1.js

            exec_js = execjs.compile(jscode)
            zse93 = exec_js.call('solution', [pl_url, doccookie])
            print(zse93)

        next_answer_url = self.pagejson['initialState']['question']['answers'][self.pagedata['answers_id']]['next']
        self.getpage_next_answers(next_answer_url)
    def getpage_next_answers(self,next_answer_url):
        next_answer_json= page.goto(next_answer_url).json()
        if len(next_answer_json['data'])==0:
            return
        for answeritem in next_answer_json['data']:
            answer={}
            answer['id']=answeritem['target']['id']
            answer['text'] = BeautifulSoup(answeritem['target']['content'], 'lxml').get_text(separator=' ',strip=True)
            self.pagedata['answers_objs'].append(answer)
        self.getpage_next_answers(next_answer_json['paging']['next'])

def getpage_task(url, context):
    zhihu = ZhiHu()
    zhihu.getpage(url, context)
    # 爬评论
    for answer in zhihu.pagedata['answers_objs']:
        answer_id = answer['id']
        pl_url = f"https://www.zhihu.com/api/v4/comment_v5/answers/{answer_id}/root_comment?order_by=score&limit=20&offset="
        doccookie =zhihu.page.evaluate("""() => {
            return document.cookie
        }""")
        #调js
        exec_js = execjs.compile("")
        zse93 =exec_js.call('solution', [pl_url, doccookie])

if __name__ == '__main__':

    #获取当前代码文件所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #拼接文件路径
    user_data_dir = os.path.join(current_dir, 'userdata')


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
            user_data_dir=user_data_dir,
            accept_downloads=True,
            headless=False
        )
        context.add_init_script(path='./stealth.min.js')
        #登录
        page = context.new_page()
        page.goto("https://www.zhihu.com")
        # 假设登录成功后页面上会出现用户名元素，例如一个id为'username'的标签
        dengdai=True
        while dengdai:
            page.wait_for_load_state('networkidle')
            login_button = page.query_selector_all('button:text("登录/注册")')
            if login_button:
                print("尚未登录")
                page.wait_for_timeout(1000)
            else:
                print("已登录或元素不存在")
                dengdai=False
        print("登录成功")
        #---------------------------

        for url in question_urls:
            getpage_task(url, context)
        # ---------------------
        context.close()
        print(datas_pagedata)


