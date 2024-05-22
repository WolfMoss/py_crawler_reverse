
import ctypes
import io
import os.path
import time
from functools import reduce
from multiprocessing import Pool

import numpy
import numpy as np
import cv2
import requests
import win32con
import win32gui
import win32ui


# 测试耗时
def test_run_time(func):
    def inner(*args, **kwargs):
        t_start = time.time()
        res = func(*args, **kwargs)
        t_end = time.time()
        print(f"一共花费了{t_end - t_start}秒时间,函数运行结果是 {res}")
        return res

    return inner


# 判断字符串是否为中文
def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


class DM:
    def __init__(self, path=None):
        if path:
            self.img = self.__imread(path)
        # else:
        #     self.img = self.create_random_img(1920, 1080, 3)
        self.path = None
        self.maxNum = None  # 数字模板数量
        self.hwnd= None
        self.display = "normal"
        self.mouse = "normal"
        self.keypad = "normal"
        self.mode = 0


    # 随机创建图片,用于测试算法
    def create_random_img(self, width, height, item=3):
        img = np.random.randint(0, 255, (width, height, item))
        img = img.astype(np.uint8)
        return img

    # 转换大漠格式"ffffff-303030" 为 遮罩范围(100,100,100),(255,255,255)
    def __color_to_range(self, color, sim):
        if sim <= 1:
            if len(color) == 6:
                c = color
                weight = "000000"
            elif "-" in color:
                c, weight = color.split("-")
            else:
                raise "参数错误"
        else:
            raise "参数错误"
        # color = int(c[:2], 16), int(c[4:], 16), int(c[2:4], 16)
        # weight = int(weight[:2], 16), int(weight[2:4], 16), int(weight[4:], 16)
        color = int(c[4:], 16), int(c[2:4], 16), int(c[:2], 16)
        weight = int(weight[4:], 16), int(weight[2:4], 16), int(weight[:2], 16)
        sim = int((1 - sim) * 255)
        lower = tuple(map(lambda c, w: max(0, c - w - sim), color, weight))
        upper = tuple(map(lambda c, w: min(c + w + sim, 255), color, weight))
        return lower, upper

    def __imread(self, path):
        # 读取图片
        if is_chinese(path):
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)  # 避免路径有中文
        else:
            img = cv2.imread(path)
        return img

    def __inRange(self, img, lower, upper):
        mask = cv2.inRange(img, np.array(lower), np.array(upper))
        img = cv2.bitwise_and(img, img, mask=mask)
        return img

    def __imgshow(self, img):
        windows_name = "img"
        cv2.imshow(windows_name, img)
        cv2.waitKey()
        cv2.destroyWindow(windows_name)

    def __ps_to_img(self, img, ps):
        """
        :param img: cv图像
        :param ps: 偏色
        :return: 偏色后的cv图像
        """
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        if not ps:
            return img

        elif type(ps) == str:
            lower, upper = self.__color_to_range(ps, 1)
            img = self.__inRange(img, lower, upper)

        elif type(ps) == tuple:
            lower, upper = ps
            img_hsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img = self.__inRange(img_hsv1, lower, upper)
        return img

    # 截取图像范围
    def __cutOut(self,x1,y1,x2,y2):
        if sum([x1,y1,x2,y2])==0:
            return self.img
        height,width = self.img.shape[:2]
        if y1<=y2<=height and x1<=x2<=width:
            return self.img[y1:y2,x1:x2]
        else:
            raise "x1,y1,x2,y2图像范围溢出"

    def __FindPic(self, x1, y1, x2, y2, pic_name, delta_color, sim, method, drag=None):
        # 读取图片
        img1 = self.__cutOut(x1, y1, x2, y2)
        img2 = self.__imread(self.path + os.path.sep + pic_name)

        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        img1 = self.__ps_to_img(img1, delta_color)
        img2 = self.__ps_to_img(img2, delta_color)
        # 利用cv的模板匹配找图
        result = cv2.matchTemplate(img1, img2, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        yloc, xloc = np.where(result >= sim)
        height, width = img2.shape[:2]
        return result,min_val, max_val, min_loc, max_loc,yloc, xloc,height, width

    def __normal_capture(self):
        pass

    def __windows_capture(self):
        # pip install pywin32 -i https://pypi.douban.com/simple
        # 获取窗口宽，高
        x, y, x2, y2 = win32gui.GetWindowRect(self.hwnd)
        width = x2 - x
        height = y2 - y
        # 截图
        hWndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        # 保存图片转cv图像
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
        im_opencv.shape = (height, width, 4)
        img = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)
        # 释放内存
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hWndDC)
        return img
    # 设置路径
    def SetPath(self, path):
        self.path = path

    # 单点比色
    @test_run_time
    def CmpColor(self, x, y, color, sim=1):
        """
        :param x: 坐标x
        :param y: 坐标y
        :param color: 颜色字符串,可以支持偏色,"ffffff-202020",最多支持一个
        :param sim:相似度(0.1-1.0) (0,255)
        :return:bool
        """
        lower, upper = self.__color_to_range(color, sim)
        if not lower is None:
            new_color = self.img[x, y]
            for i in [0, 1, 2]:
                if new_color[i] < lower[i] or new_color[i] > upper[i]:
                    return False
            return True
        return False

    # 范围找色
    def FindColor(self, x1, y1, x2, y2, color, sim, dir=None):
        lower, upper = self.__color_to_range(color, sim)
        img = self.__cutOut(x1, y1, x2, y2)
        height, width = img.shape[:2]
        b, g, r = cv2.split(img)
        b = b.reshape(1, height * width)
        g = g.reshape(1, height * width)
        r = r.reshape(1, height * width)
        key1 = np.where(lower[0] <= b)
        key2 = np.where(lower[1] <= g)
        key3 = np.where(lower[2] <= r)
        key4 = np.where(upper[0] >= b)
        key5 = np.where(upper[1] >= g)
        key6 = np.where(upper[2] >= r)

        if len(key1[0]) and len(key2[0]) and len(key3[0]) and len(key4[0]) and len(key5[0]) and len(key6[0]):
            keys = reduce(np.intersect1d, [key1, key2, key3, key4, key5, key6])  # 相似度越小,交集数据越多,找的慢,相似度越大,找的越快,主要耗时的地方
            if len(keys):
                x, y = divmod(keys[1], width)
                print(img[x, y])
                return 0, x + x1, y + y1
        return -1, -1, -1

    # 找图
    def FindPic(self, x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None):
        """
        :param x1:区域的左上X坐标
        :param y1:区域的左上Y坐标
        :param x2:区域的右下X坐标
        :param y2:区域的右下Y坐标
        :param pic_name:图片名，只能单个图片
        :param delta_color:偏色,可以是RGB偏色,格式"FFFFFF-202020",也可以是HSV偏色，格式((0,0,0),(180,255,255))
        :param sim:相似度，和算法相关
        :param dir:算法，总共有6总
        :param drag:是否在找到的位置画图并显示,默认不画
               方差匹配方法：匹配度越高，值越接近于0。
               归一化方差匹配方法：完全匹配结果为0。
               相关性匹配方法：完全匹配会得到很大值，不匹配会得到一个很小值或0。
               归一化的互相关匹配方法：完全匹配会得到1， 完全不匹配会得到0。
               相关系数匹配方法：完全匹配会得到一个很大值，完全不匹配会得到0，完全负相关会得到很大的负数。
                    （此处与书籍以及大部分分享的资料所认为不同，研究公式发现，只有归一化的相关系数才会有[-1,1]的值域）
               归一化的相关系数匹配方法：完全匹配会得到1，完全负相关匹配会得到-1，完全不匹配会得到0。
        :return:
        """
        result,min_val, max_val, min_loc, max_loc,yloc, xloc,height, width = self.__FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None)
        if len(xloc):
            x, y = max_loc[0] + x1, max_loc[1] + y1
            if drag:
                img = cv2.rectangle(self.img, (x, y), (x + width, y + height), (255, 0, 0), thickness=2)
                self.__imgshow(img)
            return 0, x, y
        return -1, -1, -1

    # 找图，返回多个匹配地址
    def FindPics(self,x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None):
        result,min_val, max_val, min_loc, max_loc,yloc, xloc,height, width = self.__FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None)
        if len(xloc):
            if drag:
                for loc in  zip(xloc,yloc):
                    img = cv2.rectangle(self.img, (loc[0], loc[1]), (loc[0] + width, loc[1] + height), (255, 0, 0), thickness=2)
                    self.__imgshow(img)
            return 0,zip(xloc,yloc)
        return -1,[-1,-1]

    # 查找数字是否存在
    def FindNum(self, x1, y1, x2, y2, numString, color_format, sim):
        """
        :param x1: x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param numString: 字符串:如数字"1","56","789"
        :param color_format:字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV,以及灰度格式都支持.
        :param sim: 双精度浮点数:相似度,取值范围0.1-1.0
        :return:bool
        """
        if numString in str(self.OcrNum(x1, y1, x2, y2, color_format, sim)):
            return True
        return False

    # 识别数字
    def OcrNum(self, x1, y1, x2, y2, color_format, sim,dirPath):
        """
        :param x1:  x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param color_format: 字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV,以及灰度格式都支持.
        :param sim: 双精度浮点数:相似度,取值范围0.1-1.0
        :param dirPath: 图库路径,用于存储0-9数字模板
        :return: num：字符串数字
        """
        num_dict = {}
        # 遍历图像,并挨个识别
        for i in range(10):
            img_num = dirPath + os.path.sep + f"{i}.bmp"
            ret, locs = self.FindPics(x1, y1, x2, y2, img_num, color_format, sim)
            if ret != -1:
                for loc in locs:
                    num_dict.update({loc[0]: i})
        # 排序字典
        new_num_list = sorted(num_dict.items(), key=lambda x: x[0])# 对x轴进行排序

        # 遍历并拼接数字
        nums = "".join([str(new_num[1]) for new_num in new_num_list])
        try:
            return nums
        except:
            return ""

    # 服务器ocr
    def OcrServer(self, x1, y1, x2, y2, color_format, sim):
        """
        :param x1: 整形数:区域的左上X坐标
        :param y1: 整形数:区域的左上Y坐标
        :param x2: 整形数:区域的右下X坐标
        :param y2: 整形数:区域的右下Y坐标
        :param color_format: 偏色,可以是RGB偏色,格式"FFFFFF-202020",也可以是HSV偏色，格式((0,0,0),(180,255,255))
        :param sim: 相似度
        :return: 列表,包含坐标和文字
        """
        if not None in [x1,y1,x2,y2]:
            img = self.img[y1:y2, x1:x2]
        img = self.__ps_to_img(img, color_format)
        img_bt = np.array(cv2.imencode('.png', img)[1]).tobytes()
        file = io.BytesIO(img_bt)
        data = {
            'username': 270207756,
            'pwd': 123456,
            'lang': "ch",  # ch中文,eh英文
            "det": True,  # 是指是否要检测文本的位置,False为识别单行，Ture为识别多行，只有多行才有坐标返回
            "ret": True,  # 是指是否要识别文本的内容
        }
        response = requests.post('http://150.158.53.154:9000/login', files=[('img', ("", file))], data=data)
        if response.status_code == 200:
            result = response.json()
            msg_code = result["msg_code"]
            if msg_code == 200:
                content = result["content"]
                result = [item for item in content[0] if item[1][1] > sim]
                new_result = []
                for item in result:
                    item[0] = [[loc[0] + x1, loc[1] + y1] for loc in item[0]]
                    new_result.append(item)
                return new_result
            else:
                print(f"识别异常 {response.json()}")

        else:
            print(f"服务器异常 {response.status_code}")
            return False

    def BindWindow(self,hwnd,display,mouse,keypad,mode=0):
        self.hwnd= hwnd
        self.display = display
        self.mouse = mouse
        self.keypad = keypad
        self.mode = mode

    # 截图
    def Capture(self,x1, y1, x2, y2, file=None):
        """
        :param x1: x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param file: 保存文件路径，不填写则写入cv图像到属性self.img
        :return:
        """
        # 截图
        if self.display == "normal":
            self.img = self.__normal_capture()
        elif self.display == "windows":
            self.img = self.__windows_capture()
        # 截取并写入
        img = self.__cutOut(x1, y1, x2, y2)
        if not img is None:
            if file:cv2.imwrite(file,img)
            else:self.img = img
            return 1
        return 0


if __name__ == '__main__':
    # dm = DM()
    # 单点比色
    # dm.CmpColor(100, 200, "888888-505050", 0.9)
    # 范围找色
    # dm.FindColor(0, 0, 1920 - 1, 1080 - 1, "ffff00-404040", 1, 0)
    # 找图
    # dm = DM(r"E:\code\python\demo\功能\算法\鼠标原图6.png")
    # dm.SetPath(r"E:\code\python\demo\功能\算法")
    # print(dm.FindPic(0, 0, 960, 540, "鼠标手1.bmp", ((0, 0, 221), (180, 30, 255)), 0.9, 5, True))

    # # 测试ocr功能
    # dm = DM(r"E:\code\python\demo\功能\算法\鼠标原图6.png")
    # result = dm.OcrServer(0, 0, 960, 540, '', 0.8)
    # print(result)

    # # 测试速度
    # 小图 = r"E:\code\python\demo\功能\算法\小图.bmp"
    # 大图 = r"E:\code\python\demo\功能\算法\鼠标原图6.png"
    # dm = DM(大图)
    # p_num = 10
    # task_num = 20
    # p = Pool(p_num)
    # s = time.time()
    # for i in range(task_num):
    #     p.apply_async(dm.OcrServer, args=(0, 0, 960, 540, "", 0.7,))
    # p.close()
    # p.join()
    # print(f"并发{p_num},总请求{task_num},总耗时{time.time() - s}")

    # 测试OcrNum
    # dm = DM(r"E:\code\python\demo\功能\算法\token_test\010.bmp")
    # dm.SetPath(r"E:\code\python\demo\功能\算法")
    # num = dm.OcrNum(0,0,0,0,"",0.95,"token_num")
    # print(num)

    #截图
    dm = DM()
    dm.BindWindow(657562,"windows","windows","windows",0)
    if dm.Capture(0,0,0,0):
        cv2.imshow("img",dm.img)
        cv2.waitKey()


