from paddleocr import PaddleOCR, draw_ocr
import time
import cv2
import numpy as np
import mss
from PIL import Image
import io
import mss.tools
import pygetwindow as gw
import pyautogui
ocr = PaddleOCR()




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

window = find_window_by_title("图片查看")
x, y, width, height = window.left, window.top, window.width, window.height
monitor = {
    'left': x,
    'top': y,
    'width': width,
    'height': height
}
#----------------------------------------------

# 预加载所有需要找图的模板图+++++++++++++++++++++++++++++
template_path = '1.png'
# 读取模板图像和目标图像
template = cv2.imread(template_path, 0)
#----------------------------------------------

#定义方法+++++++++++++++++++++++++++++++++++++++
def movemouse(location):
    pyautogui.moveTo(location[0] + 10, location[1] + 10)
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
                lefttop=(box[0][0]+x,box[0][1]+y)
                return lefttop

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

    # # 计算模板图像的宽度和高度
    # w, h = template.shape[::-1]
    # 根据最大值位置绘制矩形框，标识出匹配位置
    #top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv2.rectangle(target, top_left, bottom_right, 255, 2)
    #
    # # 显示结果
    #
    # cv2.namedWindow('Matching Result', cv2.WINDOW_NORMAL)
    # cv2.imshow('Matching Result', target)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 返回匹配位置的绝对坐标
    lefttop=(max_loc[0]+x,max_loc[1]+y)
    return lefttop

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
get_color_ratio(monitor,[0, 120, 70],[10, 255, 255])
#----------------------------------------------