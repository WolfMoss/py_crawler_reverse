from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
import codecs


def scroll_to_bottom(page):
    page.evaluate("""() => {
        return  new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 500;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        })
    }""")

if __name__ == '__main__':

    # 打开并读取HTML文件
    with codecs.open('1.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 解析HTML内容
    html_tree = etree.HTML(html_content)
    # 提取类名为"content"的div元素内的文本
    content_divs = html_tree.xpath('//a[@data-za-detail-view-id="3942"]/@href')

    question_urls=[] #问题帖子集合
    p_urls=[] #专栏文章集合

    for content in content_divs:
        if content.startswith("//zhuanlan.zhihu.com"):
            content = "https:"+content
            p_urls.append(content)
        elif content.startswith("/question"):
            content = "https://www.zhihu.com"+content
        answer_index = content.find('answer')
        if answer_index != -1:
            content= content[:answer_index-1]
            question_urls.append(content)
    print(question_urls,p_urls)

    for url in question_urls:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(storage_state="auth.json")
            page = context.new_page()
            page.goto(url)

            page.wait_for_timeout(1000)
            scroll_to_bottom(page)

            content = page.content()
            print(content)
            # ---------------------
            context.close()
            browser.close()



