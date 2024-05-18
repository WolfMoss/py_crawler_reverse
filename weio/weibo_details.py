import execjs
import requests
import py_moss_helper
import json
import os
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree

#先搜索https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E5%8E%9F%E7%A5%9E
#用https://m.weibo.cn/api/container/getIndex?接口获取返回的搜索结果，取"bid": "OeDerFN44"
#详情地址https://weibo.cn/comment/OeDerFN44

# 获取当前代码文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接文件路径
user_data_dir = os.path.join(current_dir, 'userdata')

with sync_playwright() as playwright:
    # browser = playwright.chromium.connect_over_cdp('http://localhost:8899/')
    # context = browser.contexts[0]
    browser = playwright.chromium
    context = browser.launch_persistent_context(
        user_data_dir=user_data_dir,
        accept_downloads=True,
        headless=False,
        bypass_csp=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    )
    context.add_init_script(path='./stealth.min.js')
    # 登录
    gpage = context.new_page()
    gpage.goto("https://m.weibo.cn/")
    dengdai = True
    while dengdai:
        cookies = gpage.context.cookies('https://m.weibo.cn')

        # 遍历 cookies 查找 key 为 'MLOGIN' 的字段值
        for cookie in cookies:
            if cookie['name'] == 'MLOGIN':
                mlogin_cookie_value = cookie['value']
                if mlogin_cookie_value == '1':
                    print("登录成功")
                    dengdai = False
                    break
                else:
                    print("尚未登录")
                    gpage.wait_for_timeout(1000)
                    continue

    print(dengdai)