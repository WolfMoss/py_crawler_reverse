import requests
session = requests.Session()
import execjs
import py_moss_helper
import json
from playwright.sync_api import Playwright, sync_playwright, expect


url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=Java&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=1&pageSize=30&page=1"
#
# payload = {}
# headers = {
#   'accept': 'application/json, text/plain, */*',
#   'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
#   'x-requested-with': 'XMLHttpRequest'
# }
# response = session.request("GET", url, headers=headers, data=payload)
# print(response.json())
# name= response.json()['zpData']['name']
# seed= response.json()['zpData']['seed']
# ts= response.json()['zpData']['ts']

with sync_playwright() as playwright:
  # browser = playwright.chromium.connect_over_cdp('http://localhost:8899/')
  # context = browser.contexts[0]
  browser = playwright.chromium
  context = browser.launch_persistent_context(
    user_data_dir=py_moss_helper.Helper.get_userdata_path(),
    accept_downloads=True,
    headless=False,
    bypass_csp=True
  )
  context.add_init_script(path='./stealth.min.js')
  # 登录
  gpage = context.new_page()

  gpage.goto("https://www.zhipin.com/web/geek/job?query=Java&city=101010100&page=1")
  try:
    gpage.wait_for_load_state('networkidle',timeout=10000)
  except Exception as e:
    print(f"Page loading timed out: {e}")

  gpage.add_script_tag(path="./2.js")

  #获取cookie
  cookies = gpage.context.cookies('https://www.zhipin.com')
  cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': cookie_string
  }

  page = context.new_page()
  res = page.request.get(url, headers=headers)

  set_cookie_headers = res.headers['set-cookie']
  __zp_sseed__ = set_cookie_headers.split(';')[0].split('=')[1] + '='
  __zp_sts__ = set_cookie_headers.split('__zp_sts__=')[1].split(';')[0]
  print('__zp_sseed__:::', __zp_sseed__)
  print('__zp_sts__:::', __zp_sts__)
  __zp_stoken__ = gpage.evaluate(f"window.MF('{__zp_sseed__}',{__zp_sts__})")
  print(__zp_stoken__)


  #循环2-10
  for i in range(1,11):
    url = f"https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=Java&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=1&pageSize=30&page={i}"
    res = page.request.get(url, headers=headers)
    print(res.json()['zpData']['jobList'])
    set_cookie_headers = res.headers['set-cookie']
    __zp_sseed__=set_cookie_headers.split(';')[0].split('=')[1] + '='
    __zp_sts__=set_cookie_headers.split('__zp_sts__=')[1].split(';')[0]
    print('__zp_sseed__:::',__zp_sseed__)
    print('__zp_sts__:::', __zp_sts__)
    __zp_stoken__ =gpage.evaluate(f"window.MF('{__zp_sseed__}',{__zp_sts__})")
    print(__zp_stoken__)
    headers['cookie'] = __zp_stoken__


  context.close()
