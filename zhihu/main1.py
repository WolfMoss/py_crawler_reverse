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
            pl_url = "https://www.zhihu.com/api/v4/comment_v5/answers/3246747600/root_comment?order_by=score&limit=20&offset="
            cookies = self.page.context.cookies('https://www.zhihu.com')
            cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
            #cookie_string = '_zap=a0bd719d-cf14-44fd-94ca-a1838a5ec147; d_c0=APBWZW7knhiPTqPOjEjzXRVKGrdAenGCgOA=|1715759942; gdxidpyhxdE=UCET%2B2mcbb%5C5Acc7gSVWh7L%2B8NwagRor8YVhffC%5CzAmHqH3lfhPTW%2Bdumx%5CWvNa8%5CBAqOpr7cJ78%5C712hybwUNK%5CSNZshyIBUvyCKeatuIQaG2oP6tnqmAopOUqvYxLUq%2B3%5CfYuyJxJq0kI%5CI%2FdrKn2V5AKvqjwfJqnmrdh9kWdzsNja%3A1715760845563; captcha_session_v2=2|1:0|10:1715760110|18:captcha_session_v2|88:WVFDWDFYSGZOaFJLakNaTWFtK2lRaGlMdFpYMGVxQUxTM1hMWCt4RmpDaVpUbzM5amR5Q2dNK05hV2s3a2lUNA==|8ff2b160bd4c1c7e8dacc3d6d62998b2e6ea057adf03f382629ebb81e86ecfba; __snaker__id=0xnH4NvDoBbuSjiK; q_c1=2d16b6a89d004e5986da7f3c9eb6b2e6|1715760117000|1715760117000; z_c0=2|1:0|10:1715760196|4:z_c0|92:Mi4xUVBTcUhnQUFBQUFBOEZabGJ1U2VHQ1lBQUFCZ0FsVk45Ymt4WndBa1J3cXd1NzZPS0lrRTQ0bGhtejlTMzJKZlJn|daae1da354d70abf7678fcfd4ff472da0303dbc59dadfa9f158d653c5148aeb4; BEC=d5e2304fff7e4240174612484fe7ffa4; _xsrf=49798e8c-fa0e-457e-bfe8-c50a424f3ded; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1715760127,1715760195,1715760216,1715760324; SESSIONID=tuCcISGMFyAsVTj7keOKKwjIbghFARWI8nISm8LBUEL; JOID=U1kSCkpo7eDuXYPfVmAdcHwpb0FIHJ6thRTQnhUulKeTA9e1Z6mJooBdhddQokMAaVGj98BVECOHfTywHkOeDL8=; osd=UVkUB0Jq7ebjVYHfUG0VcnwvYklKHJigjRbQmBgmlqeVDt-3Z6-EqoJdg9pYoEMGZFmh98ZYGCGHezG4HEOYAbc=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1715760328; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1715760370|1715760323; _xsrf=22HTlYCR9fGNfOqQuy24LoSiER31u8tq; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1715760979|1715760323'
            # 调js
            zse96 = exec_js.call('solution', [pl_url, cookie_string])
            self.page.set_extra_http_headers({
                'x-zse-93': '101_3_3.0',
                'x-zse-96': zse96,
                'cookie': cookie_string
            })
            headers = {
                'cookie': cookie_string,
                'x-zse-93': '101_3_3.0',
                'x-zse-96': zse96
            }

            response = requests.request("GET", pl_url, headers=headers)
            a = self.page.goto(pl_url)
            print(zse96)

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
        #ckobj = page.goto("https://www.zhihu.com/search?type=content&q=%E6%8B%9B%E6%8A%95%E6%A0%87%E5%9B%A0%E4%B8%BAip%E7%9B%B8%E5%90%8C%E8%A2%AB%E5%A4%84%E7%BD%9A")
        #---------------------------

        for url in question_urls:
            getpage_task(url, context)
        # ---------------------
        context.close()
        print(datas_pagedata)


