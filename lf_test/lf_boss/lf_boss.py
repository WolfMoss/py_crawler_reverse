import time

import requests
session = requests.Session()
import py_moss_helper
from playwright.sync_api import Playwright, sync_playwright, expect
import ctypes
import win32con


user32 = ctypes.windll.user32
def enum_windows():
  EnumWindows = user32.EnumWindows
  EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                       ctypes.POINTER(ctypes.c_int),
                                       ctypes.POINTER(ctypes.c_int))
  GetWindowText = user32.GetWindowTextW
  GetWindowTextLength = user32.GetWindowTextLengthW
  IsWindowVisible = user32.IsWindowVisible
  windows = []

  def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
      length = GetWindowTextLength(hwnd)
      buf = ctypes.create_unicode_buffer(length + 1)
      GetWindowText(hwnd, buf, length + 1)
      windows.append((hwnd, buf.value))
    return True

  EnumWindows(EnumWindowsProc(foreach_window), 0)
  return windows


# 获取包含特定标题的窗口句柄
def get_window_handle(partial_title):
  windows = enum_windows()
  for hwnd, title in windows:
    if partial_title.lower() in title.lower():
      return hwnd
  return None


# 隐藏窗口
def hide_window(hwnd):
  # SW_HIDE: 0 - Hide the window
  ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_HIDE)


  # 设置窗口样式，使其透明和不可见
  ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, win32con.GWL_EXSTYLE)
  ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW
  ctypes.windll.user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE, ex_style)
  ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA)


# 显示窗口
def show_window(hwnd):
  # SW_SHOW: 5 - Activates the window and displays it in its current size and position.
  ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_SHOW)


url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=Java&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=1&pageSize=30&page=1"

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
  gpage = context.pages[0]
  gpage.evaluate("() => { document.title = 'Custom Window Title'; }")
  gpage.wait_for_timeout(100)
  window_title = "Custom Window Title"  # 谷歌浏览器窗口的标题，可以部分匹配
  hwnd = get_window_handle(window_title)
  if hwnd:
    print(f"Found window handle: {hwnd}")
    hide_window(hwnd)
    print("Window hidden")
  else:
    print("Window not found")

  gpage.goto("https://www.zhipin.com/web/geek/job?query=Java&city=101010100&page=1")
  try:
    gpage.wait_for_load_state('networkidle',timeout=10000)
  except Exception as e:
    print(f"Page loading timed out: {e}")




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


  #循环2-10
  for i in range(2,5):

    with open('pack20240626.js', 'r', encoding='utf-8') as file:
        js_code = file.read()
    # 在页面中执行 JavaScript 文件
    gpage.evaluate(js_code)
    cookies = gpage.context.cookies('https://www.zhipin.com')
    for c in cookies:
      if c['name'] == '__zp_stoken__':
        print('__zp_stoken__===', c['value'])
    cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
    headers['cookie'] = cookie_string

    url = f"https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=Java&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page={i}&pageSize=30"
    res = page.request.get(url, headers=headers)
    #打印时间，精确到毫秒
    print('当前时间===',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '；本页数据===',res.json()['zpData']['jobList'])
    #print('本页数据===',res.json()['zpData']['jobList'])

    #延迟1秒
    page.wait_for_timeout(1000)

  context.close()
