from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
import codecs


def scroll_to_bottom(page):
    SCROLL_PAUSE_TIME = 0.5  # 设置滚动后暂停的时间，给页面加载新内容的时间

    # 获取当前滚动高度
    last_height = page.evaluate("document.body.scrollHeight")

    while True:
        # 滚动到当前页面底部
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

        # 等待页面加载新内容
        page.wait_for_timeout(int(SCROLL_PAUSE_TIME * 1000))

        # 再次获取滚动高度，与上次比较
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            # 如果滚动高度不再变化，说明可能已经滚动到底部
            break
        last_height = new_height
def run(playwright: Playwright,url) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    page.goto(url)

    page.wait_for_timeout(2000)
    scroll_to_bottom(page)

    content = page.content()
    print(content)
    # ---------------------
    context.close()
    browser.close()

# 打开并读取HTML文件
with codecs.open('1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析HTML内容
html_tree = etree.HTML(html_content)
# 提取类名为"content"的div元素内的文本
content_divs = html_tree.xpath('//a[@data-za-detail-view-id="3942"]/@href')

question_urls=[]
p_urls=[]

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
        run(playwright,url)



