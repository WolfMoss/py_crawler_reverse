#pyinstaller -F main.py --add-data "Resource\ARegJ64.dll;Resource" --add-data "Resource\AoJia64.dll;Resource"
import json
import time
import cv2
import leidian
import yanzheng
import os
import wmi
c = wmi.WMI()
import pyperclip
from win32com.client import Dispatch
import ctypes
from tkinter import messagebox
import requests
import threading
from tkinter import Tk

yanzheng.method_name()

root = Tk()
root.withdraw()  # 隐藏主窗口


current_dir = os.path.dirname(os.path.abspath(__file__))
ARegJ = ctypes.windll.LoadLibrary(os.path.join(current_dir,'Resource\ARegJ64.dll'))
ARegJ.SetDllPathW(os.path.join(current_dir,'Resource\AoJia64.dll'), 0)
global AJ
AJ = Dispatch('AoJia.AoJiaD')
print(AJ.VerS())

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


# 预加载所有需要找图的模板图+++++++++++++++++++++++++++++
leidianindex = config['leidianindex']
h_pai = '1.PNG'
h_pai_template = cv2.imread(h_pai, 0)
png2 = os.path.join(current_dir,'2.png')
#----------------------------------------------

def send_notification(tz_str):
    """
    发送Server酱通知
    :param tz_str: 通知的标题内容
    """
    # Server酱的SCKEY，这里需要替换为您自己的SCKEY
    SCKEY = "SCT249952TXIFKYY5Hl0Z9PAeHzl3Aht35"
    api_url = f"https://sctapi.ftqq.com/{SCKEY}.send"

    # 准备POST数据
    data = {
        "title": tz_str,
        # 如果需要，您也可以添加"desp"字段来描述通知的详细内容
        # "desp": "这里是通知的详细描述",
    }

    try:
        response = requests.post(api_url, data=data)
        response_json = response.json()

        if response_json["code"] == 0:
            print("通知发送成功！")
        else:
            print(f"通知发送失败，错误信息：{response_json['message']}")
    except Exception as e:
        print(f"发送通知时发生错误：{e}")

def send_notification2(tz_str):
    """
    发送Server酱通知
    :param tz_str: 通知的标题内容
    """
    # Server酱的SCKEY，这里需要替换为您自己的SCKEY
    SCKEY = "SCT250078TrATwIQ1OqzfaHN8qxuRGvbIg"
    api_url = f"https://sctapi.ftqq.com/{SCKEY}.send"

    # 准备POST数据
    data = {
        "title": tz_str,
        # 如果需要，您也可以添加"desp"字段来描述通知的详细内容
        # "desp": "这里是通知的详细描述",
    }

    try:
        response = requests.post(api_url, data=data)
        response_json = response.json()

        if response_json["code"] == 0:
            print("通知发送成功！")
        else:
            print(f"通知发送失败，错误信息：{response_json['message']}")
    except Exception as e:
        print(f"发送通知时发生错误：{e}")



def find_image(template,target):

    # 应用模板匹配
    res = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    # 获取匹配结果的最大值和位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #print(max_val, max_loc)

    # 返回匹配位置的绝对坐标
    if max_val>0.8:
        lefttop=(max_loc[0],max_loc[1])
        return lefttop
    else:
        return False

def closeexe():
    # 程序结束
    AJ.GBHouTai()
    os._exit(0)


# Dnconsole.launch(1)
# time.sleep(2)
#print(Dnconsole.list_running()[0])
Hwnd1 = (str(leidian.Dnconsole.list_running()[0])).split('bind:')[1].split(' ')[0]
#十六进制转十进制
Hwnd = int(Hwnd1, 16)
#print('LDHwnd===',Hwnd)



p = AJ.KQHouTai(Hwnd, 'OL', 'DX', 'DX', '', 3)


pots = [
    {'zb':(106,210),
     'tongzhi':0
     },
    {'zb':(280,210),
     'tongzhi':0
     },
    {'zb':(455,210),
     'tongzhi':0
     },
    {'zb':(106,380),
     'tongzhi':0
     }
]

xunhnum = len(pots)

def dopot(index):
    pot=pots[index]
    #扫一扫
    AJ.MoveTo(71, 170)
    AJ.LeftClick()
    time.sleep(0.5)
    #选择相册
    AJ.MoveTo(491, 72)
    AJ.LeftClick()
    time.sleep(0.5)

    # 根据类名TrayNoticeWindow获取句柄
    TrayNoticeHwnd = AJ.FindWindow(0, "", 0, "TrayNoticeWindow", "", 0, 0)
    #print('TrayNoticeHwnd===', TrayNoticeHwnd)
    AJ.SetWindowState(TrayNoticeHwnd, 0)

    #选择二维码
    AJ.MoveTo(pot['zb'][0], pot['zb'][1])
    AJ.LeftClick()
    time.sleep(4)


    #判断是否404
    AJ.ScreenShot(199, 713, 399, 761, png2, 1, 0, 0, 0, 1, 1)
    png2_template = cv2.imread(png2, 0)
    ploc = find_image(h_pai_template,png2_template)
    if ploc:
        pot['tongzhi']=0
        print("没量，下一个")
    else:
        if pot['tongzhi']==0:
            pot['tongzhi']=1

            # 复制链接
            AJ.MoveTo(499, 75)
            AJ.LeftClick()
            time.sleep(0.5)
            AJ.MoveTo(273, 731)
            AJ.LeftClick()
            time.sleep(0.5)

            # 获取剪切板数据
            clipboard_content =str(pyperclip.paste())
            ma_key =  clipboard_content.split('linkChannel=')[1]
            ma_name = config[ma_key]
            #发通知
            tz_str = f"{ma_name}有量！"
            #弹窗提醒
            # root.call('wm', 'attributes', '.', '-topmost', True)  # 将父窗口置顶
            # messagebox.showinfo("提示", tz_str)

            #URL编码

            # 示例调用函数
            send_notification(tz_str)
            send_notification2(tz_str)


    #返回主页
    AJ.MoveTo(34, 76)
    AJ.LeftClick()
    time.sleep(0.5)

print("开始监听...")

now_index = 0
while 1:
    if now_index >= xunhnum:
        now_index = 0

    print(now_index)
    try:
        dopot(now_index)
    except Exception as e:
        leidian.Dnconsole.stopapp(leidianindex, "com.eg.android.AlipayGphone")
        time.sleep(1)
        leidian.Dnconsole.invokeapp(leidianindex, "com.eg.android.AlipayGphone")
        time.sleep(3)
        dopot(now_index)

    now_index = now_index +1




