
import json
import os

from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
import codecs
#msedge.exe --remote-debugging-port=8899 --user-data-dir="D:\codes\py_crawler_reverse\zhihu\userdata"

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

class ZhiHu:
    def getpage(self,url, context):
        pagedata = {}
        pagedata['answers_text'] = []
        page = context.new_page()
        try:
            page.goto(url)
        except:
            print("超时", url)
        # page.wait_for_timeout(1000)
        page.wait_for_load_state("load")
        content = page.content()
        tree = etree.HTML(content)
        # 使用XPath表达式选择元素
        btn_elements = tree.xpath('//button[normalize-space(text())="显示全部"]')
        if btn_elements:
            # 直接寻找角色为button且包含文本"显示全部"的元素
            show_all_button = page.locator('button:text("显示全部")')
            show_all_button.click()
        content = page.content()
        pagedata['title'] = page.query_selector('h1').inner_text()  # 获取问题标题
        # 解析HTML字符串，创建一个HTML元素树
        tree = etree.HTML(content)
        # 使用XPath表达式选择元素
        elements = tree.xpath(
            '//div[@class="QuestionHeader"]//span[starts-with(@class, "RichText") and @itemprop="text"]/p')
        # 打印所有选中元素的文本内容
        question_text = ""
        for element in elements:
            question_text = question_text + str(element.text) if element.text is not None else ""
        pagedata['question_text'] = question_text  # 获取问题正文
        pagedata['url'] = url  # 获取问题链接
        datas_pagedata.append(pagedata)
        scroll_to_bottom(page)
        content = page.content()
        tree = etree.HTML(content)
        # 使用XPath表达式选择元素
        as_elements = tree.xpath("//div[@class='List-item'][.//button[contains(@aria-label, '赞同')]]")
        if not as_elements:
            return
        # 打印元素下面所P节点的文本内容
        for element in as_elements:
            answer_text = ""
            for p_element in element.xpath(".//p"):
                answer_text =answer_text + str(p_element.text).replace("None", "")
            pagedata['answers_text'].append(answer_text)
        print(json.dumps(pagedata, ensure_ascii=False))
        page.close()

def getpage_task(url, context):
    zhihu = ZhiHu()
    zhihu.getpage(url, context)

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


