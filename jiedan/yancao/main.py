import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests
from zoneinfo import ZoneInfo

def get_time_beijing(url):
    response = requests.get(url,verify=False)
    if response.status_code == 200:
        date_time = response.headers['Date']
        date_time_obj = datetime.strptime(date_time, '%a, %d %b %Y %H:%M:%S GMT')
        gmt_time = date_time_obj.replace(tzinfo=ZoneInfo("UTC"))
        beijing_time = gmt_time.astimezone(ZoneInfo("Asia/Shanghai"))
        return beijing_time
    else:
        return None
async def find_page_containing_url(context, url_fragment):
    # 遍历所有页面，查找包含指定 URL 片段的页面
    for page in context.pages:
        if url_fragment in page.url:
            return page
    return None
async def main():
    async with async_playwright() as p:
        # 启动 Microsoft Edge 浏览器
        browser = await p.chromium.launch(channel='msedge', headless=False,args=['--start-maximized'])
        context = await browser.new_context(viewport={"width": 1920, "height": 1080}, no_viewport=True)
        page = await context.new_page()

        # 打开一个网页
        await page.goto('https://zwfwdt.tobacco.gov.cn/cooperativeWeb/event/tab')

        while True:
            # 查找URL包含特定字符串的页面
            target_url_fragment = 'https://zwfwdt.tobacco.gov.cn/online/#/new/bidinfo.html'
            target_page = await find_page_containing_url(context, target_url_fragment)
            if target_page:
                # 在找到目标页面后，执行一些操作
                print(f"找到目标页面，请先填写好所有数据，并且让提交按钮亮起","开始等待8点...")

                beijing_time = get_time_beijing('https://zwfwdt.tobacco.gov.cn/cooperativeWeb/event/header')
                start_time = beijing_time.strftime('%H:%M:%S')
                print('当前时间===', start_time)
                start_time = datetime.strptime(start_time, '%H:%M:%S')
                end_time = datetime.strptime("08:00:00", '%H:%M:%S')  # 设定结束时间

                time_difference = end_time - start_time  # 计算时间差
                # 对于 page.wait_for_timeout(),我们需要时间差的毫秒数
                wait_time = time_difference.total_seconds() * 1000
                print("wait_time===", wait_time)
                await target_page.wait_for_timeout(wait_time)
                print("时间到，点击")
                # 点击id=newBidSubmit的<a>标签
                await target_page.click('#newBidSubmit')


                break
            else:
                print("正在等待进入提交界面...")
                # 如果没有找到目标页面，等待一段时间后再次检查
                await asyncio.sleep(1)


        await browser.close()


asyncio.run(main())