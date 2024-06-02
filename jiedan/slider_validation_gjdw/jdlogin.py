import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.edge.service import Service
#from 基本操作.PIL图片大小设置 import resize_and_save_image
#from 基本操作.下载base64图片 import dow_base
#from 基本操作.缺口识别 import identify_gap
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import os
import base64
import cv2
import uuid


def identify_gap():
    print('开始识别时间', time.asctime())
    # 读取背景图片和缺口图片
    bg_img = cv2.imread('bg.png')  # 背景图片
    tp_img = cv2.imread('tm.png')  # 缺口图片
    # 确保图片加载成功
    if bg_img is None or tp_img is None:
        print("Error: 图片未正确加载。请检查文件路径和文件完整性。")
        return None

        # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)  # 修正拼写错误
    tp_edge = cv2.Canny(tp_img, 100, 200)  # 修正拼写错误

    # 缺口匹配
    # 如果 tp_edge 太大，您可能需要先对其进行缩放
    res = cv2.matchTemplate(bg_edge, tp_edge, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

    # 绘制方框
    th, tw = tp_edge.shape[:2]
    top_left = max_loc  # 左上角点的坐标，使用英文命名
    print('结束时间', time.asctime())

    # 返回缺口的X坐标
    return top_left[0]

print(identify_gap())

def dow_base(base64_encoded_image, name):
    # 确保目录存在，如果不存在则创建它
    import os
    directory = './photo/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 解码Base64数据
    imagedata = base64.b64decode(base64_encoded_image)
    # 将解码后的数据写入文件
    with open(f'{directory}{name}', "wb") as file:
        file.write(imagedata)

    print(f'图片已保存为：{directory}{name}')

def resize_and_save_image(image_path, output_directory, output_filename, target_width,
                          target_height):
    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

        # 打开图像
    image = Image.open(image_path)

    # 如果图像是RGBA模式，转换为RGB模式
    if image.mode == 'RGBA':
        image = image.convert('RGB')

        # 调整图像尺寸
    new_img = image.resize((target_width, target_height))

    # 构建完整的输出文件路径
    output_path = os.path.join(output_directory, output_filename)

    # 保存为JPEG格式
    new_img.save(output_path)


url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fre.jd.com%2Fsearch' \
      '%3Fkeyword%3D%25e4%25ba%25ac%25e4%25b8%259c%25e5%2595%2586%25e5%259f%258e%25e7%25bd%2591' \
      '%25e4%25b8%258a%25e8%25b4%25ad%25e7%2589%25a9%25e5%25ae%25b6%25e7%2594%25b5%25e5%2586%25b0' \
      '%25e7%25ae%25b1%26keywordid%3D43620911346%26re_dcp%3D21Sm2D2ZOw%26traffic_source%3D1004' \
      '%26test%3D1%26enc%3Dutf8%26cu%3Dtrue%26utm_source%3Dhaosou-search%26utm_medium%3Dcpc' \
      '%26utm_campaign%3Dt_262767352_haosousearch%26utm_term' \
      '%3D43620911346_0_8ec077c88b154b7584c370ff4aa065fe '

# 创建一个ChromeOptions对象，用于配置Chrome浏览器的启动参数
options = ChromeOptions()

uer_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
options.add_argument('User-Agent=%s' % uer_agent)
# 添加一个实验性的选项，排除某些启动开关，这里排除了'enable-automation'开关
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument('--headless')  # 设置为无头
#options.add_argument('--disable-gpu')  # 设置没有使用gpu
#options.add_argument("--no-sandbox")
# 排除这个开关可以使浏览器在启动时不显示自动化控制的标识，有助于绕过某些网站的反爬虫机制
#options.add_argument(r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome for Testing\User Data\\')
#options.add_argument('--profile-directory=Default')
options.add_experimental_option('excludeSwitches', ['enable-automation'])

#options.add_argument('--headless')

# 使用配置好的options来初始化Chrome浏览器驱动
ser = Service()
#ser.path = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver-win64\chromedriver.exe'
ser.path = r'.\chromedriver.exe'
#ser.path = r'D:\Google\chromedriver-win64\chromedriver.exe'
#ser.path = r'C:\Users\Administrator\Downloads\chrome-win64\chrome-win64\chrome.exe'
driver = webdriver.Chrome(options=options, service=ser)

# 执行Chrome DevTools Protocol (CDP) 命令，这个命令会在每个新打开的文档上执行一段JavaScript代码
# 这段JavaScript代码的目的是重新定义window.navigator.webdriver对象的getter方法
# 将其getter方法设置为返回undefined，这意味着当网站尝试检查navigator.webdriver属性时
try:
# 它将无法得到任何值（undefined），从而隐藏了自动化控制的痕迹
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {
                           'source': 'Object.defineProperty(navigator, "webdriver",{get:() => undefined})'
                       })

    driver.get(url)
except Exception as e:
    print(repr(e))
    input()
# 填写登录信息
time.sleep(3)
driver.find_element(By.ID, 'loginname').clear()
driver.find_element(By.ID, 'loginname').send_keys('15268317813')
time.sleep(0.5)
driver.find_element(By.ID, 'nloginpwd').clear()
driver.find_element(By.ID, 'nloginpwd').send_keys('941556')
driver.implicitly_wait(3)
driver.find_element(By.ID, 'loginsubmit').click()
time.sleep(5)

# 下载图片
# 图片文件名（确保它们是唯一的，并且带上扩展名）
bg_filename = 'background.jpg'
tp_filename = 'piece.jpg'

# 尝试次数
attempts = 3
random_str = str(uuid.uuid4().hex)
file_extension = '.txt'
file_name = random_str + file_extension
def export_url(driver, url):
    # driver.refresh()
    driver.get(url)
    wait_for_page_load = "return document.readyState"
    ready_state = driver.execute_script(wait_for_page_load)

    while ready_state != 'complete':
        ready_state = driver.execute_script(wait_for_page_load)

    # 执行JavaScript来获取AJAX请求的状态
    # ajax_requests = driver.execute_script("""
    #   var requests = performance.getEntries();
    #   return requests.filter(function(request) {
    #     return (request.initiatorType === 'xmlhttprequest' || request.entryType === 'fetch');
    #   });
    # """)
    # flag = False
    # for check in ajax_requests:
    #     if check['responseStatus'] == 403:
    #         flag = True
    #         break
    # if flag:
    #     #driver.refresh()
    #     export_url(driver, url)
    #jdwl_icon = driver.find_element(by=By.CSS_SELECTOR, value='div[class="icon-wl"]')
    #jdwl_icon = EC.invisibility_of_element_located((By.CLASS_NAME,'icon-wl'))
    #a = driver.find_element(By.TAG_NAME, value='title').text
    yz_flag = False
    while True:
        a = driver.execute_script('return document.getElementsByTagName("title")[0].textContent')
        #a = driver.find_element(By.TAG_NAME, value='title').text
        if a != '京东验证':
            break
        if a.find("企业采购") != -1:
            while True:
                driver.get(url)
                time.sleep(10)
                name = driver.find_element(By.CLASS_NAME, 'nickname').text
                if name is not None and name != '':
                    print(f'{name}-用户登录成功')
                    yz_flag = True
                    break
            wait_for_page_load = "return document.readyState"
            ready_state = driver.execute_script(wait_for_page_load)
            while ready_state != 'complete':
                ready_state = driver.execute_script(wait_for_page_load)
        else:
            yz_flag = True
        # else:
        #     break
    # if yz_flag:
    if yz_flag:
        driver.refresh()
        # export_url(driver, url)
    wait_for_page_load = "return document.readyState"
    ready_state = driver.execute_script(wait_for_page_load)

    while ready_state != 'complete':
        ready_state = driver.execute_script(wait_for_page_load)

    yz_flag = False
    while True:
        a = driver.execute_script('return document.getElementsByTagName("title")[0].textContent')
        # a = driver.find_element(By.TAG_NAME, value='title').text
        if a != '京东验证':
            break
        else:
            yz_flag = True
    if yz_flag:
        driver.refresh()
        wait_for_page_load = "return document.readyState"
        ready_state = driver.execute_script(wait_for_page_load)

        while ready_state != 'complete':
            ready_state = driver.execute_script(wait_for_page_load)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    jdwl_icon = driver.execute_script('return document.getElementsByClassName("icon-wl").length')
    # if jdwl_icon is not None:
    #     print("元素存在")
    # else:
    #     print("元素不存在")
    if jdwl_icon == 1 or jdwl_icon == '1':
        return
    # spbtn = driver.find_element(By.XPATH , value='/html/body/div[9]/div[2]/div[1]/div[1]/ul/li[5]')
    # spbtn.click()
    driver.execute_script("""document.querySelector('[data-offset="38"]').click()""")
    time.sleep(2)
    yz_flag = False
    while True:
        a = driver.execute_script('return document.getElementsByTagName("title")[0].textContent')
        # a = driver.find_element(By.TAG_NAME, value='title').text
        if a != '京东验证':
            break
        else:
            yz_flag = True
    if yz_flag:
        driver.refresh()
        wait_for_page_load = "return document.readyState"
        ready_state = driver.execute_script(wait_for_page_load)

        while ready_state != 'complete':
            ready_state = driver.execute_script(wait_for_page_load)
        time.sleep(2)
        driver.execute_script("""document.querySelector('[data-offset="38"]').click()""")
        time.sleep(2)

    zwpl = driver.execute_script('return document.getElementsByClassName("ac comments-item").length')
    if zwpl == 1 or zwpl == '1':
        return
    time.sleep(2)
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    plrq = driver.execute_script("return document.getElementsByClassName('order-info')[0].textContent")
    dates = re.findall(date_pattern, plrq)
    if dates[0].find('2024') != -1:
        with open(file_name,mode='a+',encoding='utf-8') as f:
            f.write(url+'\n')

    return


    #     return
    # pj = driver.find_element(by=By.CSS_SELECTOR, value='li[class="current"][data-offset="38"]')
    # pj.click()


# for i in range(attempts):
#     try:
        # 尝试获取昵称元素的文本
while True:
    time.sleep(10)
    name = driver.find_element(By.CLASS_NAME, 'nickname').text
    print(f'{name}-用户登录成功')
    break
wait_for_page_load = "return document.readyState"
ready_state = driver.execute_script(wait_for_page_load)
while ready_state != 'complete':
    ready_state = driver.execute_script(wait_for_page_load)
# 如果找到了昵称，则关闭浏览器并退出循环
with open('urls.txt',mode='r',encoding='utf-8') as u:
    for url in u.readlines():
        url = url.replace('\n','').replace('\r','')
        export_url(driver, url)
        #export_url(driver,'https://item.jd.com/2371522.html')
        #driver.quit()
        # break
    # except NoSuchElementException:
    #     print('未找到昵称元素，尝试第', i + 1, '次')
    #
    #     # 获取图片src
    #     bg_img = driver.find_element(By.XPATH,
    #                                  '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div['
    #                                  '1]/img').get_attribute('src')
    #     tp_img = driver.find_element(By.XPATH,
    #                                  '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div['
    #                                  '2]/img').get_attribute('src')
    #     # 清洗base64
    #     bg_img = re.split(',', bg_img)[1]
    #     tp_img = re.split(',', tp_img)[1]
    #
    #     # 调用函数保存图片
    #     dow_base(bg_img, bg_filename)
    #     dow_base(tp_img, tp_filename)
    #
    #     # 改变图片大小
    #     resize_and_save_image('./photo/background.jpg', './resized_photos', 'background_new.jpg',
    #                           242, 94)
    #     resize_and_save_image('./photo/piece.jpg', './resized_photos', 'piece_new.jpg', 33, 33)
    #
        # 分析滑块距离
        total_distance = identify_gap()
        print('缺口x距离：', total_distance)
        # 获取滑块元素
        hk = driver.find_element(By.XPATH,
                                 '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[3]')
        # 创建动作链并执行滑动操作
        action = ActionChains(driver)
        action.click_and_hold(hk).perform()
        time.sleep(2)  # 等待点击和保持生效

        # 接下来执行滑动逻辑...
        # 这里添加您自己的滑动逻辑代码
        # 每次滑动的距离
        step_size = int(total_distance) / 14
        print('每次滑动的距离：', step_size)
        # 滑动的间隔时间
        interval = 1
        for j in range(14):
            if j <= 6:
                action.move_by_offset(xoffset=step_size - 1, yoffset=2).perform()
                # action.pause(interval)
            elif 6 < j <= 12:
                action.move_by_offset(xoffset=step_size + 1, yoffset=1).perform()
                # action.pause(2)
            else:
                action.move_by_offset(xoffset=step_size + 1.5, yoffset=1).perform()
                action.release().perform()  # 释放鼠标
        # 等待一段时间再进行下一次尝试
        time.sleep(3)
    # except Exception as e:
    #     print(repr(e))
    #     input()

    # 如果循环结束后仍未找到昵称元素，则退出浏览器
    # if i == attempts - 1:
    #     #driver.quit()
    #     print('尝试了', attempts, '次，仍未找到昵称元素，退出浏览器。')