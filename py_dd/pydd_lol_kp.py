from paddleocr import PaddleOCR, draw_ocr
from datetime import datetime
ocr = PaddleOCR()
import mss.tools
import pygetwindow as gw
import pyautogui
import mss
import cv2
import keyboard
import time
import asyncio
import numpy as np
from PIL import Image
import io
from ctypes import *
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
dll_path = os.path.join(cur_path, 'dd40605x64.dll')
dd_dll = windll.LoadLibrary(dll_path)
time.sleep(2)
st = dd_dll.DD_btn(0) #DD Initialize
if st==1:
    print("OK")
else:
    print("Error")
    exit(101)

# 预加载所有需要找图的模板图+++++++++++++++++++++++++++++
h_pai = 'h.PNG'
h_pai_template = cv2.imread(h_pai, 0)
#----------------------------------------------

# 获取特定窗口的标题++++++++++++++++++++++++++++++++++
# 你想要查找的窗口标题的部分字符串
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

# window = find_window_by_title("League of Legends (TM) Client")
# x, y, width, height = window.left, window.top, window.width, window.height
# monitor = {
#     'left': x,
#     'top': y,
#     'width': width,
#     'height': height
# }
#----------------------------------------------

#定义方法+++++++++++++++++++++++++++++++++++++++
#移动鼠标
def movemouse(location):
    pyautogui.moveTo(location[0] + 10, location[1] + 10)

#找字
def ocrtest(wenzi,monitor):
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)

    # 将截图转换为PIL图像，这一步取决于你的OCR方法接受什么样的输入
    img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb)

    # 如果你的OCR库可以接受图像数据流，可以如下转换
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # 这里是你的函数，例如 ocr.ocr("屏幕截图 2024-05-22 151713.png")
    result = ocr.ocr(img_byte_arr)
    for line in result:
        for result in line:
            box = result[0]
            text = result[1][0]
            confidence = result[1][1]
            if wenzi in text:
                print(f'识别到的文字: {text}, 置信度: {confidence}')
                print(f'文字坐标: {box}')
                lefttop=(box[0][0]+monitor['left'],box[0][1]+monitor['top'])
                return lefttop

#找图
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
    if max_val>0.8:
        lefttop=(max_loc[0]+monitor['left'],max_loc[1]+monitor['top'])
        return lefttop
    else:
        return False

#区域找色，返回颜色占比
def get_color_ratio(monitor,lower_redsz,upper_redsz):

    # 读取图片
    with mss.mss() as sct:
        # 截取窗口
        sct_img = sct.grab(monitor)
    # 将截图转换为OpenCV图像
    screen_img = np.array(sct_img)
    screen_img = cv2.cvtColor(screen_img, cv2.COLOR_BGRA2BGR)

    # 设定颜色的阈值范围（这里以红色为例）
    lower_red = np.array(lower_redsz)
    upper_red = np.array(upper_redsz)

    # 将ROI区域的颜色空间从BGR转换到HSV
    hsv_roi = cv2.cvtColor(screen_img, cv2.COLOR_BGR2HSV)

    # 创建掩膜
    mask = cv2.inRange(hsv_roi, lower_red, upper_red)

    # 计算掩膜中白色像素的比例
    mask_area = cv2.countNonZero(mask)
    roi_area = screen_img.shape[0] * screen_img.shape[1]
    color_ratio = (mask_area / roi_area) * 100
    # 输出颜色出现的比例
    print(f"指定颜色在ROI中出现的比例为：{color_ratio:.2f}%")
    if color_ratio > 0.5:
        # 初始化坐标
        first_red_pixel = None
        last_red_pixel = None
        # 遍历掩膜以找到红色像素的坐标
        for y in range(mask.shape[0]):
            for x in range(mask.shape[1]):
                if mask[y, x] != 0:  # 如果当前像素是红色
                    if first_red_pixel is None:
                        first_red_pixel = (x, y)  # 记录第一个红色像素的坐标
                    last_red_pixel = (x, y)  # 更新最后一个红色像素的坐标
        # 输出坐标
        if first_red_pixel and last_red_pixel:
            print(f"左上第一个红色像素的坐标为：{first_red_pixel}")
            print(f"右下最后一个红色像素的坐标为：{last_red_pixel}")
            return (first_red_pixel,last_red_pixel)
        else:
            print("没有找到红色像素")

#循环找图，超出指定秒报错
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

#循环找字，超出指定秒报错
def getpic(wenzi,monitor,max_time_seconds):
    start_time = time.time()
    getit = False
    while getit == False:
        location = ocrtest(wenzi, monitor)
        if location:
            print(f"找到{wenzi}在位置: {location}")
            getit = True
            return location
        else:
            if time.time() - start_time > max_time_seconds:
                print(f"超过最大循环时间 {max_time_seconds} 秒，未找到{wenzi}")
                return False
            time.sleep(0.1)
#------------------------------------------------------------


# #找图+++++++++++++++++++++++++++++++++++++++++++++
# location = find_image(template,monitor)
# print(f"Found template at: {location}")
# pyautogui.moveTo(location[0]+10, location[1]+10)
#----------------------------------------------

#找字+++++++++++++++++++++++++++++++++++++++++++++
# location = ocrtest("写程序",monitor)
# movemouse(location)
#----------------------------------------------

#找颜色++++++++++++++++++++++++++++++++++++++++++++
#get_color_ratio(monitor,[0, 120, 70],[10, 255, 255])
#----------------------------------------------

kapai_monitor = {
    'left': 834,
    'top': 930,
    'width': 46,
    'height': 46
}

#黄牌
def pressw():
    print("主动按下W")
    dd_dll.DD_key(302, 1)
    dd_dll.DD_key(302, 2)
    print("当前时间（时:分:秒.毫秒）：", datetime.now().strftime("%H:%M:%S.%f"))
    loczb = getpic(h_pai_template, kapai_monitor,5)
    if loczb :
        dd_dll.DD_key(302, 1)
        dd_dll.DD_key(302, 2)

def presse():
    print("主动按下W")
    dd_dll.DD_key(302, 1)
    dd_dll.DD_key(302, 2)
    print("当前时间（时:分:秒.毫秒）：", datetime.now().strftime("%H:%M:%S.%f"))
    loczb = getpic(h_pai_template, kapai_monitor,5)
    if loczb :
        dd_dll.DD_key(302, 1)
        dd_dll.DD_key(302, 2)

# 注册全局热键，当按下Ctrl+Shift+a时触发my_function
keyboard.add_hotkey('space', pressw)
keyboard.add_hotkey('e', presse)

# 进入阻塞状态，等待热键触发
keyboard.wait('esc')  # 使用esc键退出监听