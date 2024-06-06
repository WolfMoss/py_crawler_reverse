import time
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def run(playwright):
    browser = playwright.chromium.launch(headless=False,channel="msedge")
    context = browser.new_context()
    page = context.new_page()

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if current_time < "2024-06-06 8:30":
            continue

        response = page.goto('https://exchange.yuanbaokc.com/optimize.html?pageType=3&linkChannel=ZJ01_BD_202405302005009610_0006')
        # 获取当前时间，作为文件名
        now = datetime.now()
        datetime_str = now.strftime("%Y%m%d%H%M%S")
        # 将返回体和返回头保存到一个文本文件中
        with open(f'{datetime_str}.txt', 'w') as f:
            f.write("Response Body:\n")
            f.write(response.body().decode('utf-8'))  # 如果返回数据为二进制，需要适当处理
            f.write("\n-----------------\n")
            f.write("Response Headers:\n")
            for key, value in dict(response.headers).items():
                f.write(f"{key}: {value}\n")
        time.sleep(3)  # 等待3秒

    context.close()
    browser.close()

with sync_playwright() as p:
    run(p)