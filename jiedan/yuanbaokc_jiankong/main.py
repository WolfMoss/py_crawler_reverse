#pyinstaller -F main.py --add-data "Resource\ARegJ64.dll;Resource" --add-data "Resource\AoJia64.dll;Resource"
import json
import time
import cv2
from xml.dom.minidom import parseString
import shutil
import os
import wmi
c = wmi.WMI()
import socket
import pyperclip
from win32com.client import Dispatch
import ctypes
from tkinter import messagebox
import threading
from tkinter import Tk
root = Tk()
root.withdraw()  # 隐藏主窗口

#验证+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
maxi = 0
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
if current_time > "2024-06-08 15:00"  and maxi == 1:
    print("退出")
    # 结束整个程序
    os._exit(0)


hard_disk_serial_number = c.Win32_DiskDrive()[0].SerialNumber #获取CPU序列号

device_from_json={
    "mac_address": hard_disk_serial_number,
    "function_name": "validate_customer",
    "data_string": "yuanbaokc_jiankong"
}
yanzhengstr = json.dumps(device_from_json)

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def receive_all(self):
        BUFFER_SIZE = 1024
        data = b''

        while True:
            try:
                part = self.client_socket.recv(BUFFER_SIZE)
                data += part
                if len(part) < BUFFER_SIZE:
                    break
            except:
                return False


        return data.decode('utf-8')

    def send_message(self, msg):
        self.client_socket.send(msg.encode('utf-8'))
        if msg == 'exit':
            self.client_socket.close()
            return

    def start_receiving(self):
        while True:
            data = self.receive_all()
            if not data:
                break
            self.handle_response(data)

    def handle_response(self,response):
        # 在这里处理服务器返回的消息
        if response == 'exit':
            print("退出")
            # 关闭整个程序
            os._exit(0)
        self.client_socket.close()


client = Client('axiba.idnmd.top', 9999)
receiving_thread = threading.Thread(target=client.start_receiving)
receiving_thread.daemon = True
receiving_thread.start()
client.send_message(yanzhengstr)
#验证---------------------------------------------------------------------


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

#雷电方法定义++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class UserInfo(object):
    def __init__(self, text: str = ""):
        super(UserInfo, self).__init__()
        self.info = dict()
        if len(text) == 0:
            return
        self.__xml = parseString(text)
        nodes = self.__xml.getElementsByTagName('node')
        res_set = [
            # 用户信息节点
        ]
        name_set = [
            'id', 'id', 'following', 'fans', 'all_like', 'rank', 'flex',
            'signature', 'location', 'video', 'name'
        ]
        number_item = ['following', 'fans', 'all_like', 'video', 'videolike']
        for n in nodes:
            name = n.getAttribute('resource-id')
            if len(name) == 0:
                continue
            if name in res_set:
                idx = res_set.index(name)
                text = n.getAttribute('text')
                if name_set[idx] not in self.info:
                    self.info[name_set[idx]] = text
                    print(name_set[idx], text)
                elif idx == 9:
                    self.info['videolike'] = text
                elif idx < 2:
                    if len(text) == 0:
                        continue
                    if self.info['id'] != text:
                        self.info['id'] = text
        for item in number_item:
            if item in self.info:
                self.info[item] = int(self.info[item].replace('w', '0000').replace('.', ''))

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)

class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])
        self.name = info[1]
        self.top_win_handler = int(info[2])
        self.bind_win_handler = int(info[3])
        self.is_in_android = True if int(info[4]) == 1 else False
        self.pid = int(info[5])
        self.vbox_pid = int(info[6])

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)

    def __repr__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)

class Dnconsole:
    # 请根据自己电脑配置
    console = config['console']
    ld = config['ld']
    share_path = config['share_path']

    # 获取模拟器列表
    @staticmethod
    def get_list():
        #cmd = os.popen(Dnconsole.console + 'list2')

        with os.popen(Dnconsole.console + 'list2') as fp:
            bf = fp._stream.buffer.read()
        try:
            text = bf.decode().strip()
        except UnicodeDecodeError:
            text = bf.decode('gbk').strip()

        #cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(DnPlayer(dnplayer))
        return result

    # 获取正在运行的模拟器列表
    @staticmethod
    def list_running() -> list:
        result = list()
        all = Dnconsole.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result

    # 检测指定序号的模拟器是否正在运行
    @staticmethod
    def is_running(index: int) -> bool:
        all = Dnconsole.get_list()
        if index >= len(all):
            raise IndexError('%d is not exist' % index)
        return all[index].is_running()

    # 执行shell命令
    @staticmethod
    def dnld(index: int, command: str, silence: bool = True):
        cmd = Dnconsole.ld + '-s %d %s' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 执行adb命令,不建议使用,容易失控
    @staticmethod
    def adb(index: int, command: str, silence: bool = False) -> str:
        cmd = Dnconsole.console + 'adb --index %d --command "%s"' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 安装apk 指定模拟器必须已经启动
    @staticmethod
    def install(index: int, path: str):
        shutil.copy(path, Dnconsole.share_path + str(index) + '/update.apk')
        time.sleep(1)
        Dnconsole.dnld(index, 'pm install /sdcard/Pictures/update.apk')

    # 卸载apk 指定模拟器必须已经启动
    @staticmethod
    def uninstall(index: int, package: str):
        cmd = Dnconsole.console + 'uninstallapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 启动App  指定模拟器必须已经启动
    @staticmethod
    def invokeapp(index: int, package: str):
        cmd = Dnconsole.console + 'runapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        print(result)
        return result

    # 停止App  指定模拟器必须已经启动
    @staticmethod
    def stopapp(index: int, package: str):
        cmd = Dnconsole.console + 'killapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 输入文字
    @staticmethod
    def input_text(index: int, text: str):
        cmd = Dnconsole.console + 'action --index %d --key call.input --value %s' % (index, text)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 获取安装包列表
    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = Dnconsole.dnld(index, 'pm list packages')
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result

    # 检测是否安装指定的应用
    @staticmethod
    def has_install(index: int, package: str):
        if Dnconsole.is_running(index) is False:
            return False
        return package in Dnconsole.get_package_list(index)

    # 启动模拟器
    @staticmethod
    def launch(index: int):
        cmd = Dnconsole.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 关闭模拟器
    @staticmethod
    def quit(index: int):
        cmd = Dnconsole.console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置屏幕分辨率为1080×1920 下次启动时生效
    @staticmethod
    def set_screen_size(index: int):
        cmd = Dnconsole.console + 'modify --index %d --resolution 1080,1920,480' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 点击或者长按某点
    @staticmethod
    def touch(index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            Dnconsole.dnld(index, 'input tap %d %d' % (x, y))
        else:
            Dnconsole.dnld(index, 'input touch %d %d %d' % (x, y, delay))

    # 滑动
    @staticmethod
    def swipe(index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    # 复制模拟器,被复制的模拟器不能启动
    @staticmethod
    def copy(name: str, index: int = 0):
        cmd = Dnconsole.console + 'copy --name %s --from %d' % (name, index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 添加模拟器
    @staticmethod
    def add(name: str):
        cmd = Dnconsole.console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置自动旋转
    @staticmethod
    def auto_rate(index: int, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = Dnconsole.console + 'modify --index %d --autorotate %d' % (index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变设备信息 imei imsi simserial androidid mac值
    @staticmethod
    def change_device_data(index: int):
        # 改变设备信息
        cmd = Dnconsole.console + 'modify --index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变CPU数量
    @staticmethod
    def change_cpu_count(index: int, number: int):
        # 修改cpu数量
        cmd = Dnconsole.console + 'modify --index %d --cpu %d' % (index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def get_cur_activity_xml(index: int):
        # 获取当前activity的xml信息
        Dnconsole.dnld(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(1)
        f = open(Dnconsole.share_path + '/activity.xml', 'r', encoding='utf-8')
        result = f.read()
        f.close()
        return result


    # 获取当前activity名称
    @staticmethod
    def get_activity_name(index: int):
        text = Dnconsole.dnld(index, '"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    # 等待某个activity出现
    @staticmethod
    def wait_activity(index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if Dnconsole.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False

    # 找图
    @staticmethod
    def find_pic(screen: str, template: str, threshold: float):
        try:
            scr = cv2.imread(screen)
            tp = cv2.imread(template)
            result = cv2.matchTemplate(scr, tp, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val < threshold:
                print(template, min_val, max_val, min_loc, max_loc)
                return False, None
            print(template, min_val, min_loc)
            return True, min_loc
        except Exception as e:
            print('An error occurred:', e)
            return False, None



    # 等待某个图片出现
    @staticmethod
    def wait_picture(index: int, timeout: int, template: str) -> bool:
        count = 0
        while count < timeout:
            Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
            time.sleep(2)
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '\\apk_scr.png', template, 0.8)
            if ret is False:
                print(loc)
                time.sleep(2)
                count += 2
                continue
            print(loc)
            return True
        return False

    # 在当前屏幕查看模板列表是否存在,是返回存在的模板,如果多个存在,返回找到的第一个模板
    @staticmethod
    def check_picture(index: int, templates: list):
        Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
        time.sleep(1)
        for i, t in enumerate(templates):
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '\\apk_scr.png', t, 0.8)
            if ret is True:
                return i, loc
        return -1, None

    @staticmethod
    def get_user_info(index: int) -> UserInfo:
        xml = Dnconsole.get_cur_activity_xml(index)
        usr = UserInfo(xml)
        if 'id' not in usr.info:
            return UserInfo()
        return usr

#雷电方法定义----------------------------------------------------------


# Dnconsole.launch(1)
# time.sleep(2)
#print(Dnconsole.list_running()[0])
Hwnd1 = (str(Dnconsole.list_running()[0])).split('bind:')[1].split(' ')[0]
#十六进制转十进制
Hwnd = int(Hwnd1, 16)
#print('LDHwnd===',Hwnd)

Dnconsole.invokeapp(leidianindex,"com.eg.android.AlipayGphone")
time.sleep(2)

AJ.KQHouTai(Hwnd, 'GDI', 'DX', 'DX', 'LAA|LAM', 3)


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
            root.call('wm', 'attributes', '.', '-topmost', True)  # 将父窗口置顶
            messagebox.showinfo("提示", tz_str)


    #返回主页
    AJ.MoveTo(34, 76)
    AJ.LeftClick()
    time.sleep(0.5)

print("开始监听...")

now_index = 0
def timer():

    global now_index

    if now_index >= xunhnum:
        now_index = 0
    dopot(now_index)

    now_index = now_index +1
    #下面这行代码会每隔0.1秒执行一次timer方法
    threading.Timer(0.1, timer).start()

timer()   #启动的时候执行一次





