#pyinstaller slider_validation.spec

import asyncio
import json
import pygetwindow as gw
from playwright.async_api import async_playwright
import base64
import mss
import numpy as np
import pyautogui
import time
import cv2
from io import BytesIO
from PIL import Image
import os
import yanzheng

yanzheng.method_name("gjdw")



# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

gpage = None

# 预加载所有需要找图的模板图+++++++++++++++++++++++++++++

h_pai = os.path.join(script_dir, 'hk.PNG')
h_pai_template = cv2.imread(h_pai, 0)
dlpng = os.path.join(script_dir, 'dl.PNG')
dlpng_template = cv2.imread(dlpng, 0)
#----------------------------------------------

def find_window_by_title(partial_title):
    # 获取当前打开的所有窗口
    all_windows = gw.getAllWindows()
    # 过滤出包含部分标题的窗口
    filtered_windows = [win for win in all_windows if partial_title in win.title]
    # 如果找到了匹配的窗口，可以选择第一个窗口
    if filtered_windows:
        window = filtered_windows[0]
        print(f"找到窗口: {window.title}")
        return window
    else:
        raise Exception("没有找到匹配的窗口。")

def find_image(template,monitor):

    with mss.mss() as sct:
        # 截取窗口
        sct_img = sct.grab(monitor)
    # 将截图转换为OpenCV图像
    screen_img = np.array(sct_img)
    screen_img = cv2.cvtColor(screen_img, cv2.COLOR_BGRA2BGR)
    # 确保目标图像也是灰度的，如果不是则进行转换
    target = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)

    # 应用模板匹配
    res = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    # 获取匹配结果的最大值和位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_val, max_loc)

    # 返回匹配位置的绝对坐标
    if max_val>0.6:
        lefttop=(max_loc[0]+monitor['left'],max_loc[1]+monitor['top'])
        return lefttop
    else:
        return False

def getpic(template, monitor,max_time_seconds):
    start_time = time.time()
    getit = False
    while getit == False:
        location = find_image(template, monitor)
        if location:
            print(f"找到图片在位置: {location}")
            getit = True
            return location
        else:
            if time.time() - start_time > max_time_seconds:
                print(f"超过最大循环时间 {max_time_seconds} 秒，未找到图片")
                return False
            time.sleep(0.1)

def _tran_canny(image):
    # 在这里你可以添加任何图像处理操作，如Canny边缘检测
    return cv2.Canny(image, 100, 200)
def base64_to_cv2(base64_str):
    # 解码base64字符串为二进制数据
    image_data = base64.b64decode(base64_str)
    # 将二进制数据转换为PIL图像
    image = Image.open(BytesIO(image_data))
    # 将PIL图像转换为OpenCV图像
    opencv_image = cv2.cvtColor(np.array(image), cv2.IMREAD_GRAYSCALE)
    #opencv_image = np.array(image)
    return opencv_image

def find_gap_center(background_img_path, template_img_path):
    # 解码Base64字符串并打开图像
    image_data = base64.b64decode(template_img_path)
    image = Image.open(BytesIO(image_data)).convert("RGBA")
    datas = image.getdata()
    new_data = []
    for item in datas:
        # 更改白色背景（可以调整容差）
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))  # 将白色像素变为透明
        else:
            new_data.append(item)
    image.putdata(new_data)
    # 转换为NumPy数组以便进一步处理
    arr = np.array(image)
    # 获取非透明像素的边界
    non_white_pixels = np.where(arr[:, :, 3] != 0)
    if non_white_pixels[0].size == 0 or non_white_pixels[1].size == 0:
        return None  # 如果没有非白色像素，返回None或其他适当的值
    # 获取边界值
    top, bottom = np.min(non_white_pixels[0]), np.max(non_white_pixels[0])
    left, right = np.min(non_white_pixels[1]), np.max(non_white_pixels[1])
    # 裁剪图像
    cropped_image = image.crop((left, top, right + 1, bottom + 1))
    # 将图像转换为Base64字符串
    buffered = BytesIO()
    cropped_image.save(buffered, format="PNG")
    tmbase64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    #print(tmbase64_image)


    # 读取背景图和模板图
    template = base64_to_cv2(tmbase64_image)
    background = base64_to_cv2(background_img_path)

    # 获取模板图像的宽度
    template_height, template_width = template.shape[:2]
    #print(f"模板图像宽度: {template_width}, 高度: {template_height}")

    # 使用模板匹配来找到缺口位置
    result = cv2.matchTemplate(background, template, cv2.TM_CCOEFF_NORMED)

    # 获取匹配结果中最大值的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print('max_val===',max_val)
    # 缺口的左上角位置
    top_left = max_loc

    return top_left[0]+template_width/2


#方法--------------------------------------------------------------------------

async def gpageaaaaa():
    print("运行gpageaaaaa")
    global gpage
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])  # headless=False 便于调试
        gcontext = await browser.new_context(viewport={"width": 1920, "height": 1080}, no_viewport=True)
        stealth = os.path.join(script_dir, 'stealth.min.js')
        await gcontext.add_init_script(path=stealth)
        gpage = await gcontext.new_page()
        await gpage.goto("https://95598.cn/osgweb/login")
        # 最小化窗口
        browser_window = gw.getWindowsWithTitle("95598")[0]  # Replace with the actual title
        browser_window.minimize()

        try:
            await gpage.wait_for_load_state('networkidle',timeout=10000)
        except Exception as e:
            print(f"Page loading timed out: {e}")

        page_js = os.path.join(script_dir, 'page.js')
        await gpage.add_script_tag(path=page_js)
        # 等待脚本加载并检查函数是否可用
        await gpage.wait_for_function("() => typeof window.axibafuc1 === 'function'")

        # 修改窗口标题
        await gpage.evaluate("() => { document.title = 'Custom Window Title'; }")

        # # 获取浏览器窗口并将其置于最前面
        # browser_window = gw.getWindowsWithTitle('95598')[0]
        # browser_window.activate()

        await capture_image_requests()

async def capture_image_requests():
    print("运行capture_image_requests")

    global gpage
    async with async_playwright() as p:
        # browser = await p.chromium.launch_persistent_context(headless=False,
        #                                                      args=['--start-maximized']
        #                                                      )
        # context = await browser.new_context(viewport={"width": 1920, "height": 1080}, no_viewport=True)
        # page = await context.new_page()
        # await page.goto("https://95598.cn/osgweb/login")

        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        stealth = os.path.join(script_dir, 'stealth.min.js')
        await context.add_init_script(path=stealth)
        # # 获取所有页面
        # pages = context.pages
        # # 遍历每个页面并检查标题是否包含 "95598"
        # for pageitem in pages:
        #     title = await pageitem.title()
        #     if "95598" in title:
        #         page=pageitem

        # window = find_window_by_title("Google Chrome")
        # x, y, width, height = window.left, window.top, window.width, window.height
        monitor = {
            'left': 0,
            'top': 0,
            'width': 1920,
            'height': 1080
        }
        print(monitor)
        # 定义响应拦截处理函数
        async def log_response(response):

            request = response.request
            if request.url.startswith("https://95598.cn/api/osg-web0004/open/c44/f05"):
                page = context.pages[0]
                await  page.wait_for_timeout(5000)
                # body = await response.body()
                # # 将字节序列解码为字符串
                # body_str = body.decode('utf-8')
                # # 将字符串解析为 JSON 对象
                # try:
                #     body_json = json.loads(body_str)
                # except json.JSONDecodeError:
                #     print(f"无法解析响应体为 JSON: {body_str}")
                # print("encryptData===",body_json['encryptData'])
                # print("keycode===",request.headers['keycode'])
                # imgres= await gpage.evaluate('({ arg1, arg2 }) => window.axibafuc1(arg1, arg2)', {'arg1': body_json['encryptData'], 'arg2': request.headers['keycode']})

                print("page===",await page.title())
                # 使用 JavaScript 从 canvas 中提取图像数据
                canvas_data = await page.evaluate('''() => {
                    const canvases = document.querySelectorAll('canvas');
                    const dataURIs = [];
                    canvases.forEach(canvas => {
                        dataURIs.push(canvas.toDataURL());
                    });
                    return dataURIs;
                }''')

                print(len(canvas_data))

                try:
                    imgresjson = {}
                    imgresjson['bj']=canvas_data[0]
                    imgresjson['tm'] = canvas_data[1]

                    xpoit = find_gap_center(str(imgresjson['bj']).replace('data:image/png;base64,',''), str(imgresjson['tm']).replace('data:image/png;base64,',''))
                    xpoit=xpoit-23

                    loczb = find_image(h_pai_template, monitor)
                    print(loczb)
                    #await asyncio.sleep(10)

                    if loczb:
                        x=loczb[0]+10
                        y=loczb[1]+10

                        # 移动鼠标到元素的中心位置
                        pyautogui.moveTo(x, y, duration=0.1)
                        # 鼠标按下
                        pyautogui.mouseDown()
                        pyautogui.moveTo(x+xpoit, y, duration=1)
                        #鼠标松开
                        pyautogui.mouseUp()
                    else:
                        print("滑块元素未找到")
                except Exception as e:
                    print(e)
                    loc_dl = find_image(dlpng_template, monitor)
                    x = loc_dl[0]
                    y = loc_dl[1]
                    pyautogui.moveTo(x, y, duration=0.1)
                    await asyncio.sleep(0.01)
                    pyautogui.mouseDown()
                    await asyncio.sleep(0.01)
                    pyautogui.mouseUp()



        # 设置拦截器
        context.on("response", log_response)

        print("启动成功，可以开始UIBOT程序")

        try:
            # 保持浏览器和页面打开状态
            while True:
                await asyncio.sleep(1)  # 防止阻塞事件循环
        except KeyboardInterrupt:
            print("Stopped listening for image requests.")
            await browser.close()

# 主程序入口
if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    asyncio.run(capture_image_requests())