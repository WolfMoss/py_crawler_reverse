import threading
import time
import json
import uuid
import re
import hashlib
import winreg

import wmi
import os
import signal
import win32api
import win32con
import ctypes.wintypes
import binascii
import inspect
import requests
from enum import IntEnum
from typing import List

try:
    from arc4 import ARC4
    from Crypto.Cipher import DES
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import algorithms
except:
    os.system('pip3 install arc4 pycryptodome cryptography')
    from arc4 import ARC4
    from Crypto.Cipher import DES
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import algorithms


# 在我们安装完crypto库之后出现No module named "Crypto"的报错信息。
# 1.在python安装目录的Lib\site-packages目录里把crypto文件夹重命名为Crypto
# 2.继续调用Crypto库出现No module named 'Crypto.Cipher'的报错信息，此时我们去Crypto文件夹下看，是否存在Cipher文件夹，这时你会发现，咦，没有。
# 3.pip install pycryptodome就行了。


class BusinessType(IntEnum):
    # 软件初始化
    iniSoftInfo = 1
    # 账号注册
    accountRegister = 2
    # 账号登录
    accountLogin = 3
    # 卡密登录
    cardLogin = 4
    # 心跳
    heartBeat = 5
    # 扣点
    bucklePoint = 6
    # 退出登录
    loginOut = 7
    # 获取软件变量
    getremoteVar = 8
    # 解绑机器码
    unbundMac = 9
    # 修改用户密码
    updPwd = 10
    # 生成测试卡密
    createCard = 11
    # 开通/续费卡密
    openRenewCardNum = 12
    # 开通/续费账号
    openRenewAccount = 13
    # 卡密详情
    cardDetail = 14
    # 账号详情
    accountDetail = 15
    # 获取软件价格列表
    softPriceList = 16
    # 购买卡密
    buyCardNum = 17
    # 修改卡密/账号备注
    updRemark = 18
    # 充值卡充值
    rechCardRenewCardOrAccount = 19
    # 充值卡详情
    rechCardNumDetail = 20
    # 远程算法转发
    remoteCalculate = 21
    # 禁用还是删除：单码或账号
    disableCardOrAccount = 22


class Result:
    code: int = -998
    msg: str = ""
    data: str = ""


class Rk结果心跳失败类:
    错误编码: int = 0
    错误消息: str = ""


class Rk通讯加密方式枚举类(IntEnum):
    DES加密 = 1
    RC4加密 = 3


class Rk禁用还是删除枚举类(IntEnum):
    禁用 = 0
    删除 = 1


class Rk初始化软件入参类:
    平台用户编码: str = ""
    软件编码: str = ""
    通讯加密方式: Rk通讯加密方式枚举类 = Rk通讯加密方式枚举类.DES加密
    加密Key: str = ""
    签名盐: str = ""
    软件版本号: str = ""
    心跳失败的回调函数 = None


class Rk软件信息类:
    软件公告: str = ""
    软件基础数据: str = ""
    软件名称: str = ""
    咨询官网: str = ""
    咨询qq: str = ""
    咨询微信: str = ""
    咨询电话: str = ""
    软件logo图标地址: str = ""
    软件当前最新版本号: str = ""
    软件更新的网盘地址: str = ""
    网盘提取码: str = ""
    软件是否强制更新 = False
    换绑扣除值: int = 0
    单台设备最大登录数量: int = 0
    软件消耗类型: str = ""
    登录方式: str = ""
    登录限制: str = ""
    换绑限制: str = ""


class Rk软件价格详情类:
    价格类型ID: str = ""
    价格类型名称: str = ""
    可使用值: int = 0
    使用值单位: str = ""
    售价: int = 0
    角色ID: str = ""
    角色名: str = ""


class Rk结果基础类:
    错误编码: int = -999
    错误消息: str = "服务器访问失败，您本地网络不顺畅，请检查下（或许您用了代理IP了，当时的代理IP不稳定？）"
    服务器时间戳: int = 0


class Rk结果初始化软件类(Rk结果基础类):
    软件信息: Rk软件信息类 = None
    软件价格列表: List[Rk软件价格详情类] = None


class Rk结果单码登录类(Rk结果基础类):
    到期时间: str = ""
    剩余点数: int = 0
    角色ID: str = ""
    角色名称: str = ""
    终端客户的qq: str = ""
    终端客户的微信: str = ""
    终端客户的支付宝: str = ""
    终端客户的手机号: str = ""
    终端客户的邮箱: str = ""
    备注: str = ""
    开通的价格类型ID: str = ""
    开通的价格类型名称: str = ""


class Rk结果账号登录类(Rk结果基础类):
    到期时间: str = ""
    剩余点数: int = 0
    角色ID: str = ""
    角色名称: str = ""
    终端客户的qq: str = ""
    终端客户的微信: str = ""
    终端客户的支付宝: str = ""
    终端客户的手机号: str = ""
    终端客户的邮箱: str = ""
    备注: str = ""
    开通的价格类型ID: str = ""
    开通的价格类型名称: str = ""


class Rk结果单码详情类(Rk结果基础类):
    到期时间: str = ""
    剩余点数: int = 0
    开通的价格类型ID: str = ""
    开通的价格类名称: str = ""
    终端用户的qq: str = ""
    终端用户的微信: str = ""
    终端用户的支付宝: str = ""
    终端用户的手机号: str = ""
    终端用户的邮箱: str = ""
    备注: str = ""
    是否已开通 = False
    是否已激活 = False
    机器码: str = ""


class Rk结果账号详情类(Rk结果基础类):
    到期时间: str = ""
    剩余点数: int = 0
    开通的价格类型ID: str = ""
    开通的价格类名称: str = ""
    终端用户的qq: str = ""
    终端用户的微信: str = ""
    终端用户的支付宝: str = ""
    终端用户的手机号: str = ""
    终端用户的邮箱: str = ""
    备注: str = ""
    是否已开通 = False
    是否已激活 = False
    机器码: str = ""


class Rk结果充值卡详情类(Rk结果基础类):
    所属软件: str = ""
    可使用值: str = 0
    消耗类型: str = ""
    使用状态: str = ""


class Rk结果扣点类(Rk结果基础类):
    剩余点数: int = 0


class Rk结果解绑机器码类(Rk结果基础类):
    到期时间: str = ""
    剩余点数: int = 0


class Rk结果获取远程变量类(Rk结果基础类):
    变量值: str = ""

class Rk结果获取远程算法类(Rk结果基础类):
    算法结果: str = ""


class RkVar:
    varname: str = ""
    varvalue: str = ""


global lockInitSDK
global lockReq
global lockiniSoft
global lockLogin
global lockheartbeat
global lockloginout
global lockdetail
global lockregaccount
global lockupdaccount
global lockrech
global lockrechdetail
global lockpoint
global lockremarks
global lockunbundmac
global lockgetvarvalue
global lockdisable
lockInitSDK = threading.Lock()
lockReq = threading.Lock()
lockReqHeartBeat= threading.Lock()
lockiniSoft = threading.Lock()
lockLogin = threading.Lock()
lockheartbeat = threading.Lock()
lockloginout = threading.Lock()
lockdetail = threading.Lock()
lockregaccount = threading.Lock()
lockupdaccount = threading.Lock()
lockrech = threading.Lock()
lockrechdetail = threading.Lock()
lockpoint = threading.Lock()
lockremarks = threading.Lock()
lockunbundmac = threading.Lock()
lockgetvarvalue = threading.Lock()
lockgetcalvalue = threading.Lock()
lockdisable = threading.Lock()


def __async_raise(thread_Id, exctype):
    # 在子线程内部抛出一个异常结束线程
    # 如果线程内执行的是unittest模块的测试用例， 由于unittest内部又异常捕获处理，所有这个结束线程
    # 只能结束当前正常执行的unittest的测试用例， unittest的下一个测试用例会继续执行，只有结束继续
    # 向unittest中添加测试用例才能使线程执行完任务，然后自动结束。
    thread_Id = ctypes.c_long(thread_Id)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, None)
        raise SystemError("PyThreadState_SEtAsyncExc failed")


def terminator(thread):
    # 结束线程
    try:
        __async_raise(thread.ident, SystemExit)
    except:
        ss = ""


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        lockInitSDK.acquire()
        if not hasattr(cls, '_inst'):
            try:
                cls._inst = super(Singleton, cls).__new__(cls)
            except:
                cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        lockInitSDK.release()
        return cls._inst


class RkSDK(Singleton):
    __maccode = ""  # 机器码
    __config = {}
    __heartbeatReviceError = None
    __encrypttypeid = 0
    __encryptKey = ""
    __signSalt = ""
    __LoginList: List[str] = []
    __RkVarList: List[RkVar] = []
    __isIniSoft = False
    __瑞科_软件编码_Md5 = ""
    __currentLoginPwd = ""
    __heartbeatThread: threading.Thread = None

    __loginToken = ""
    __currentLoginCardOrAccount = ""
    __heartbeatKey = ""
    __isLogin = False
    __isLoginOut = False
    __isStartHeartBeat = False
    __isStopHeartBeat = False

    初始化软件结果属性 = None

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        padder = padding.PKCS7(algorithms.AES.block_size // 2).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def __encrypt(self, text: str) -> str:
        result = ""
        if self.__encrypttypeid == 1:
            try:
                text = self.pkcs7_padding(text.encode('utf-8'))
                result = str(binascii.b2a_hex(self.__encryptor.encrypt(text)), "utf-8")
            except:
                result = ""
        elif self.__encrypttypeid == 3:
            try:
                arc4 = ARC4(self.__encryptKey)
                result = str(binascii.b2a_hex(arc4.encrypt(text.encode())), "utf-8")
            except:
                result = ""

        return result

    def __decrypt(self, text: str) -> str:
        result = ""
        if self.__encrypttypeid == 1:
            try:
                b = binascii.a2b_hex(text.encode("utf-8"))
                decrypted_text = str(self.__decryptor.decrypt(b), 'utf-8').replace('\0', '') \
                    .replace('\x01', '').replace('\x02', '').replace('\x03', '') \
                    .replace('\x04', '').replace('\x05', '').replace('\x06', '') \
                    .replace('\x07', '').replace('\x08', '').replace('\x09', '') \
                    .replace('\x0a', '').replace('\x0b', '').replace('\x0c', '') \
                    .replace('\x0d', '').replace('\x0e', '').replace('\x0f', '').replace('\x10', '')
                return decrypted_text
            except:
                result = ""
        elif self.__encrypttypeid == 3:
            try:
                arc4 = ARC4(self.__encryptKey)
                b = binascii.a2b_hex(text.encode("utf-8"))
                result = arc4.decrypt(b)
            except:
                result = ""
        return result

    def __GetMacCode(self):
        cpuMd5 = ""
        s = wmi.WMI()
        cp = s.Win32_Processor()

        for u in cp:
            if u.ProcessorId is not None:
                cpuMd5 = hashlib.md5(u.ProcessorId.encode('utf-8')).hexdigest()
                break

        if cpuMd5 == "":
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                value, _ = winreg.QueryValueEx(key, "MachineGuid")
                machineGuid = str(value)
                cpuMd5 = hashlib.md5(machineGuid.encode('utf-8')).hexdigest()
            except Exception as e:
                print("无法获取机器码:", str(e))

        macCode = (cpuMd5[11:14] + cpuMd5[7:10] + cpuMd5[3:6] + cpuMd5[(len(cpuMd5) - 3):]).upper()
        # print("机器码:", macCode)
        return macCode

    def __GetErrorMsg(self, errorCode: int, msg: str = ""):
        result = ""
        if errorCode == -1:
            result = "软件出错，请联系客服"
        elif errorCode == -2:
            result = "请先调用：初始化软件函数"
        elif errorCode == -3:
            result = "通讯加密方式【你瑞后后台选择什么样的加密方式，此处就填写相对应的加密方式】：只能填写1或3  【1：DES加密  3:RC4加密】"
        elif errorCode == -4:
            result = "请先登录成功后再调用此函数"
        elif errorCode == -5:
            result = "单码登录函数：需要登录的单码不能为空"
        elif errorCode == -6:
            result = "账号登录函数：需要登录的账号和密码都不能为空"
        elif errorCode == -7:
            result = "请先调用退出登录函数，然后才能再次登录"
        elif errorCode == -8:
            result = "当前登录的单码或账号已登录过了【" + msg + "】，请更新一个新的单码或账号再重新登录"
        elif errorCode == -9:
            result = "初始化软件入参：心跳失败的回调函数不能为空"
        elif errorCode == -10:
            result = "注册的账号和密码不能为空"
        elif errorCode == -11:
            result = "注册的账号和密码长度都不能超过15个字符"
        elif errorCode == -12:
            result = "账号，旧密码，新密码都不能为空"
        elif errorCode == -13:
            result = "账号，旧密码，新密码长度都不能超过15个字符"
        elif errorCode == -14:
            result = "被充值的" + msg + ",充值卡号都不能为空"
        elif errorCode == -15:
            result = "查询的充值卡不能为宽"
        elif errorCode == -16:
            result = "备注内容不能为空"
        elif errorCode == -17:
            result = "备注内容不能大于500个字符"
        elif errorCode == -18:
            result = "需要解绑的" + msg + "不能为空"
        elif errorCode == -19:
            result = "变量名不能为空"
        elif errorCode == -20:
            result = "算法ID不能为空"
        elif errorCode == -21:
            result = "提交的参数不能为空"
        return result

    def __mySleep(self, sleepTime):
        loopNum = 0
        while self.__isStopHeartBeat == False and loopNum < sleepTime * 60:
            time.sleep(1)
            loopNum = loopNum + 1

    def __comeBackErrorHeartBeat(self, **kargcs):
        rk结果心跳失败 = Rk结果心跳失败类()
        rk结果心跳失败.错误编码 = kargcs["错误编码"]
        rk结果心跳失败.错误消息 = kargcs["错误消息"]
        self.__heartbeatReviceError(rk结果心跳失败)

    def __getDocPath(pathID=5):
        '''默认返回我的文档路径，buf为空则返回当前工作路径'''
        result = ""
        try:
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, pathID, None, 0, buf)
            result = os.dirname(os.realpath(__file__)) if buf.value == '' else buf.value
        except:
            result = ""

        try:
            if result == "" or result == None:
                result = os.getenv("HOME")
        except:
            result = ""
        try:
            if result == "" or result == None:
                result = os.getenv("HOMEPATH")
        except:
            result = ""

        try:
            if result == "" or result == None:
                result = os.environ["HOME"]
        except:
            result = ""

        try:
            if result == "" or result == None:
                result = os.environ["HOMEPATH"]
        except:
            result = ""

        if result == None:
            result = ""
        if result != "" and result != None:
            result = "c:" + result + "\\Documents"
        return result

    def __getToken(self, cardNumOrAccount):
        token = ""
        try:
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\rkyz\\' + self.__瑞科_软件编码_Md5, 0,
                                      win32con.KEY_ALL_ACCESS)
            tokenTemp = win32api.RegQueryValueEx(key, cardNumOrAccount)
            if len(tokenTemp) > 0:
                token = tokenTemp[0]
            win32api.RegCloseKey(key)
            if token != "":
                return token
        except:
            token = ""

        content = ""
        try:
            DocPath = self.__getDocPath()
            filePath = ""
            if DocPath != "":
                filePath = DocPath + "\\l\\" + self.__瑞科_软件编码_Md5 + "\\" + hashlib.md5(
                    cardNumOrAccount.encode()).hexdigest() + "\\t.txt"
            if filePath == "":
                filePath = os.getcwd() + "\\l\\" + self.__瑞科_软件编码_Md5 + "\\" + hashlib.md5(
                    cardNumOrAccount.encode()).hexdigest() + "\\t.txt"

            if filePath != "" and os.path.exists(filePath):
                fileContent = open(filePath, 'r')
                content = fileContent.readline()
                fileContent.close()
        except:
            token = ""

        if content != "":
            content = self.__decrypt(content)
            if content != None and content != "":
                try:
                    content = content.decode("utf-8")
                except:
                    token = ""
                temp = content.split(",")
                if len(temp) == 2:
                    if self.__maccode == temp[0]:
                        token = temp[1]

        return token

    def __saveToken(self, cardNumOrAccount: str, token: str):
        writeContent = self.__maccode + "," + token
        key = None
        try:
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\', 0, win32con.KEY_ALL_ACCESS)
        except:
            ss = ""

        if key != None:
            try:
                win32api.RegCreateKey(key, 'rkyz\\' + self.__瑞科_软件编码_Md5)
            except:
                ss = ""

            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\rkyz\\' + self.__瑞科_软件编码_Md5, 0,
                                          win32con.KEY_ALL_ACCESS)
                win32api.RegSetValueEx(key, cardNumOrAccount, 0, win32con.REG_SZ, writeContent)
                win32api.RegCloseKey(key)
            except:
                ss = ""

        try:
            DocPath = self.__getDocPath()
            filePath = ""
            if DocPath != "":
                filePath = DocPath + "\\l\\" + self.__瑞科_软件编码_Md5 + "\\" + hashlib.md5(
                    cardNumOrAccount.encode()).hexdigest()
            if filePath == "":
                filePath = os.getcwd() + "\\l\\" + self.__瑞科_软件编码_Md5 + "\\" + hashlib.md5(
                    cardNumOrAccount.encode()).hexdigest()

            if filePath != "":
                if os.path.exists(filePath) == False:
                    os.makedirs(filePath)
                filePath = filePath + "\\t.txt"
                fileContent = open(filePath, 'w')
                writeContent = self.__encrypt(writeContent)
                if writeContent != None and writeContent != "":
                    fileContent.write(writeContent)
                fileContent.close()
        except:
            ss = ""

    def __clearLogin(self):
        self.__isStartHeartBeat = False
        self.__LoginList.remove(self.__currentLoginCardOrAccount)
        self.__currentLoginCardOrAccount = ""
        self.__loginToken = ""
        self.__heartbeatKey = ""
        self.__isLogin = False
        self.__isStopHeartBeat = False

    def __getReqResultHeartBeat(self, apiUrl, ApiRequestArgs) -> Result:
        result = Result()
        result.code = -999
        result.msg = "服务器访问失败，您本地网络不顺畅，请检查下（或许您用了代理IP了，当时的代理IP不稳定？）"
        try:
            re_data = requests.post(apiUrl, json=ApiRequestArgs, verify=False).json()
            result.code = int(re_data["code"])
            result.msg = re_data["msg"]
            if result.code == 0:
                result.data = self.__decrypt(re_data["data"])
        except:
            ss = ""
        return result

    def __GetRequestResultHeartBeat(self, dataArgs, businessType: BusinessType) -> Result:
        lockReqHeartBeat.acquire()
        result = Result()
        result.code = -999
        result.msg = "服务器访问失败，您本地网络不顺畅，请检查下（或许您用了代理IP了，当时的代理IP不稳定？）"

        ApiRequestArgs = self.__config
        timestamp = int(round(time.time() * 1000))
        data_json = json.dumps(dataArgs)
        data = self.__encrypt(data_json)
        sign = hashlib.md5((str(businessType.value) + str(self.__encrypttypeid) + ApiRequestArgs['platformusercode'] +
                            ApiRequestArgs['goodscode'] +
                            ApiRequestArgs['inisoftkey'] + str(timestamp) + data + self.__signSalt + '1').encode(
            "utf-8")).hexdigest()

        ApiRequestArgs["businessid"] = businessType.value
        ApiRequestArgs["timestamp"] = timestamp
        ApiRequestArgs["data"] = data
        ApiRequestArgs["sign"] = sign

        if businessType== BusinessType.remoteCalculate:
           result = self.__getReqResultHeartBeat("http://api2.ruikeyz.com/NetVer/webapi", ApiRequestArgs)
        else:
            apiUrl="http://api.ruikeyz.com/NetVer/webapi"
            count = 0
            while count < 3:
                result = self.__getReqResultHeartBeat(apiUrl, ApiRequestArgs)
                if result.code == -999:
                    result = self.__getReqResultHeartBeat("http://api2.ruikeyz.com/NetVer/webapi", ApiRequestArgs)
                    if businessType == BusinessType.heartBeat:
                        if result.code == 1012:
                            result.code = 0

                if businessType == BusinessType.heartBeat:
                    if result.code == -999 or result.code == 1001 or result.code == 1002:
                        result.code = 0

                if result.code == -999:
                    result = self.__getReqResultHeartBeat("http://api3.ruikeyz.com/NetVer/webapi", ApiRequestArgs)

                if result.code != -999:
                    break

                time.sleep(1)
                count = count + 1
        lockReqHeartBeat.release()
        return result


    def __getReqResult(self, apiUrl, ApiRequestArgs) -> Result:
        result = Result()
        result.code = -999
        result.msg = "服务器访问失败，您本地网络不顺畅，请检查下（或许您用了代理IP了，当时的代理IP不稳定？）"
        try:
            re_data = requests.post(apiUrl, json=ApiRequestArgs, verify=False).json()
            result.code = int(re_data["code"])
            result.msg = re_data["msg"]
            if result.code == 0:
                result.data = self.__decrypt(re_data["data"])
        except:
            ss = ""
        return result

    def __GetRequestResult(self, dataArgs, businessType: BusinessType) -> Result:
        lockReq.acquire()
        result = Result()
        result.code = -999
        result.msg = "服务器访问失败，您本地网络不顺畅，请检查下（或许您用了代理IP了，当时的代理IP不稳定？）"

        ApiRequestArgs = self.__config
        timestamp = int(round(time.time() * 1000))
        data_json = json.dumps(dataArgs)
        data = self.__encrypt(data_json)
        sign = hashlib.md5((str(businessType.value) + str(self.__encrypttypeid) + ApiRequestArgs['platformusercode'] +
                            ApiRequestArgs['goodscode'] +
                            ApiRequestArgs['inisoftkey'] + str(timestamp) + data + self.__signSalt + '1').encode(
            "utf-8")).hexdigest()

        ApiRequestArgs["businessid"] = businessType.value
        ApiRequestArgs["timestamp"] = timestamp
        ApiRequestArgs["data"] = data
        ApiRequestArgs["sign"] = sign

        if businessType== BusinessType.remoteCalculate:
           result = self.__getReqResult("http://api2.ruikeyz.com/NetVer/webapi", ApiRequestArgs)
        else:
            apiUrl="http://api.ruikeyz.com/NetVer/webapi"
            count = 0
            while count < 3:
                result = self.__getReqResult(apiUrl, ApiRequestArgs)
                if result.code == -999:
                    result = self.__getReqResult("http://api2.ruikeyz.com/NetVer/webapi", ApiRequestArgs)
                    if businessType == BusinessType.heartBeat:
                        if result.code == 1012:
                            result.code = 0

                if businessType == BusinessType.heartBeat:
                    if result.code == -999 or result.code == 1001 or result.code == 1002:
                        result.code = 0

                if result.code == -999:
                    result = self.__getReqResult("http://api3.ruikeyz.com/NetVer/webapi", ApiRequestArgs)

                if result.code != -999:
                    break

                time.sleep(1)
                count = count + 1
        lockReq.release()
        return result

    def __heartbeat(self):
        lockheartbeat.acquire()
        self.__isLoginOut = False
        isExec = True
        errorNum = 0
        RepResult = Result()
        if self.__isStartHeartBeat == False:
            self.__isStartHeartBeat = True
            send_data = {
                "cardnumorusername": self.__currentLoginCardOrAccount,
                "maccode": self.__maccode,
                "token": self.__loginToken,
                "heartbeatkey": self.__heartbeatKey,
                "timestamp": 0,
                "requestflag": ""
            }
            while True:
                if self.__isStopHeartBeat:
                    isExec = False
                    break

                timestamp = int(round(time.time() * 1000))
                send_data["timestamp"] = timestamp
                send_data["requestflag"] = str(timestamp)
                RepResult = self.__GetRequestResultHeartBeat(send_data, BusinessType.heartBeat)
                if RepResult.code != 0:
                    if RepResult.code == -999 or RepResult.code == 1001 or RepResult.code == 1002 or RepResult.code == 1012:
                        if errorNum >= 12:
                            isExec = False
                            break
                        else:
                            errorNum = errorNum + 1
                            print("心跳出错，IP不稳定，再次给一次机会连接【" + str(errorNum) + "】")
                    else:
                        break
                else:
                    errorNum = 0
                    # jsonData = eval(RepResult.data)
                    # self.__heartbeatKey = jsonData["heartbeatkey"]
                    print("心跳正常运行中...")

                self.__mySleep(5)

            if isExec:
                timestamp = int(round(time.time() * 1000))
                send_data = {
                    "cardnumorusername": self.__currentLoginCardOrAccount,
                    "maccode": self.__maccode,
                    "token": self.__loginToken,
                    "timestamp": timestamp
                }
                self.__GetRequestResultHeartBeat(send_data, BusinessType.loginOut)

                rk结果心跳失败 = {
                    "错误编码": RepResult.code,
                    "错误消息": RepResult.msg
                }
                heartbeatErrorThread = threading.Thread(target=self.__comeBackErrorHeartBeat, kwargs=rk结果心跳失败)
                heartbeatErrorThread.setDaemon(True)
                heartbeatErrorThread.start()
                heartbeatErrorThread.join(60 * 30)

                self.关闭当前软件()

        self.__isStartHeartBeat = False
        print("心跳已停止")
        lockheartbeat.release()

    def 关闭当前软件(self):
        try:
            os.kill(os.getpid(), signal.SIGKILL)
        except:
            ss = ""

        try:
            os._exit(1)
        except:
            ss=""

    def 初始化软件函数(self, rk初始化软件入参: Rk初始化软件入参类) -> Rk结果初始化软件类:
        lockiniSoft.acquire()
        self.获取瑞科验证SDK当前版本号()
        result_初始化软件 = Rk结果初始化软件类()
        if self.__isIniSoft:
            lockiniSoft.release()
            return self.初始化软件结果属性

        if rk初始化软件入参.心跳失败的回调函数 == None:
            result_初始化软件.错误编码 = -9
            result_初始化软件.错误消息 = self.__GetErrorMsg(-9)
            lockiniSoft.release()
            return result_初始化软件

        if rk初始化软件入参.通讯加密方式.value != 1 and rk初始化软件入参.通讯加密方式.value != 3:
            result_初始化软件.错误编码 = -3
            result_初始化软件.错误消息 = self.__GetErrorMsg(-3)
            lockiniSoft.release()
            return result_初始化软件

        self.__maccode = self.__GetMacCode()
        self.__encrypttypeid = rk初始化软件入参.通讯加密方式.value
        self.__encryptKey = rk初始化软件入参.加密Key
        self.__signSalt = rk初始化软件入参.签名盐
        self.__heartbeatReviceError = rk初始化软件入参.心跳失败的回调函数
        self.__瑞科_软件编码_Md5 = hashlib.md5(rk初始化软件入参.软件编码.encode()).hexdigest()

        if self.__encryptKey != None and self.__encryptKey != "":
            self.__encryptKey = self.__encryptKey.encode('utf-8')
            self.__decryptor = DES.new(self.__encryptKey, DES.MODE_ECB)
            self.__encryptor = DES.new(self.__encryptKey, DES.MODE_ECB)

        self.__config = {
            "businessid": None,
            "platformusercode": rk初始化软件入参.平台用户编码,
            "goodscode": rk初始化软件入参.软件编码,
            "inisoftkey": "",
            "timestamp": None,
            "data": None,
            "encrypttypeid": rk初始化软件入参.通讯加密方式,
            "sign": "",
            "platformtypeid": 1,  # 此处写死成1
        }
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "maccode": self.__maccode,
            "versionname": rk初始化软件入参.软件版本号,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.iniSoftInfo)
        result_初始化软件.错误编码 = RepResult.code
        result_初始化软件.错误消息 = RepResult.msg

        if RepResult.code == 0:
            self.__isIniSoft = True
            result_初始化软件.软件信息 = Rk软件信息类()
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            self.__config["inisoftkey"] = jsonData["inisoftkey"]
            result_初始化软件.服务器时间戳 = int(jsonData["servertimestamp"])
            result_初始化软件.软件信息.咨询qq = jsonData["softinfo"]["consultqq"]
            result_初始化软件.软件信息.软件公告 = jsonData["softinfo"]["notice"]
            result_初始化软件.软件信息.软件名称 = jsonData["softinfo"]["softname"]
            result_初始化软件.软件信息.咨询官网 = jsonData["softinfo"]["consultwebsite"]
            result_初始化软件.软件信息.咨询微信 = jsonData["softinfo"]["consultwx"]
            result_初始化软件.软件信息.咨询电话 = jsonData["softinfo"]["consulttel"]
            result_初始化软件.软件信息.软件基础数据 = jsonData["softinfo"]["basedata"]
            result_初始化软件.软件信息.单台设备最大登录数量 = int(jsonData["softinfo"]["maxloginnum"])
            result_初始化软件.软件信息.换绑扣除值 = int(jsonData["softinfo"]["deductionconsumevalue"])
            result_初始化软件.软件信息.软件logo图标地址 = jsonData["softinfo"]["logourl"]
            if jsonData["softinfo"]["logintypeid"] == 0:
                result_初始化软件.软件信息.登录方式 = "卡密登录方式"
            else:
                result_初始化软件.软件信息.登录方式 = "账号密码登录方式"

            if jsonData["softinfo"]["consumetypeid"] == 0:
                result_初始化软件.软件信息.软件消耗类型 = "时间"
            else:
                result_初始化软件.软件信息.软件消耗类型 = "点数"

            if jsonData["softinfo"]["isoutsoftuser"] == 0:
                result_初始化软件.软件信息.登录限制 = "顶号登录"
            if jsonData["softinfo"]["isoutsoftuser"] == 1:
                result_初始化软件.软件信息.登录限制 = "不顶号登录"
            if jsonData["softinfo"]["isoutsoftuser"] == 2:
                result_初始化软件.软件信息.登录限制 = "无限制"

            if jsonData["softinfo"]["isbinding"] == 0:
                result_初始化软件.软件信息.换绑限制 = "可换绑"
            else:
                result_初始化软件.软件信息.换绑限制 = "不可换绑"
            if jsonData["softinfo"]["isforceupd"] == 1:
                result_初始化软件.软件信息.软件是否强制更新 = True
            result_初始化软件.软件信息.软件更新的网盘地址 = jsonData["softinfo"]["networkdiskurl"]
            result_初始化软件.软件信息.软件当前最新版本号 = jsonData["softinfo"]["newversionnum"]
            result_初始化软件.软件信息.网盘提取码 = jsonData["softinfo"]["diskpwd"]
            result_初始化软件.软件价格列表 = []
            for priceTemp in jsonData["softpricelist"]:
                软件价格Temp = Rk软件价格详情类()
                软件价格Temp.售价 = int(priceTemp["price"])
                软件价格Temp.角色ID = priceTemp["roleid"]
                软件价格Temp.角色名 = priceTemp["rolename"]
                软件价格Temp.可使用值 = int(priceTemp["consumevalue"])
                软件价格Temp.使用值单位 = priceTemp["consumeunit"]
                软件价格Temp.价格类型ID = priceTemp["priceid"]
                软件价格Temp.价格类型名称 = priceTemp["pricetypename"]
                result_初始化软件.软件价格列表.append(软件价格Temp)
            self.初始化软件结果属性 = result_初始化软件
        lockiniSoft.release()
        return result_初始化软件

    def 单码登录函数(self, rk需要登录的单码: str) -> Rk结果单码登录类:
        lockLogin.acquire()
        result_单码登录 = Rk结果单码登录类()
        if self.__isIniSoft == False:
            result_单码登录.错误编码 = -2
            result_单码登录.错误消息 = self.__GetErrorMsg(-2)
            lockLogin.release()
            return result_单码登录
        if self.__isLogin:
            result_单码登录.错误编码 = -7
            result_单码登录.错误消息 = self.__GetErrorMsg(-7)
            lockLogin.release()
            return result_单码登录
        if rk需要登录的单码.strip() == "":
            result_单码登录.错误编码 = -5
            result_单码登录.错误消息 = self.__GetErrorMsg(-5)
            lockLogin.release()
            return result_单码登录
        if len(self.__LoginList) > 0:
            for loginItem in self.__LoginList:
                if loginItem == rk需要登录的单码.strip():
                    result_单码登录.错误编码 = -8
                    result_单码登录.错误消息 = self.__GetErrorMsg(-8, rk需要登录的单码.strip())
                    lockLogin.release()
                    return result_单码登录
            time.sleep(2)

        if self.初始化软件结果属性.软件信息.单台设备最大登录数量 == 1:
            if len(self.__LoginList) == 0:
                token = self.__getToken(rk需要登录的单码.strip())
                if token != "":
                    timestamp = int(round(time.time() * 1000))
                    send_data = {
                        "cardnumorusername": rk需要登录的单码.strip(),
                        "maccode": self.__maccode,
                        "token": token,
                        "timestamp": timestamp
                    }
                    self.__GetRequestResult(send_data, BusinessType.loginOut)

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnum": rk需要登录的单码.strip(),
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.cardLogin)
        result_单码登录.错误编码 = RepResult.code
        result_单码登录.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            self.__isLogin = True
            self.__loginToken = jsonData["token"]
            self.__heartbeatKey = jsonData["heartbeatkey"]

            result_单码登录.备注 = jsonData["remarks"]
            result_单码登录.角色ID = jsonData["roleid"]
            result_单码登录.角色名称 = jsonData["rolename"]
            result_单码登录.终端客户的qq = jsonData["qq"]
            result_单码登录.终端客户的微信 = jsonData["wx"]
            result_单码登录.终端客户的邮箱 = jsonData["email"]
            result_单码登录.终端客户的支付宝 = jsonData["alipay"]
            result_单码登录.终端客户的手机号 = jsonData["tel"]
            result_单码登录.开通的价格类型ID = jsonData["priceid"]
            result_单码登录.到期时间 = jsonData["endtime"]
            result_单码登录.剩余点数 = jsonData["surpluspointvalue"]
            result_单码登录.开通的价格类型名称 = jsonData["pricename"]

            self.__currentLoginCardOrAccount = rk需要登录的单码
            self.__LoginList.append(self.__currentLoginCardOrAccount)
            self.__saveToken(rk需要登录的单码.strip(), self.__loginToken)

            self.__heartbeatThread = threading.Thread(target=self.__heartbeat)
            self.__heartbeatThread.setDaemon(True)
            self.__heartbeatThread.start()

        lockLogin.release()
        return result_单码登录

    def 单码详情函数(self) -> Rk结果单码详情类:
        lockdetail.acquire()
        result_单码详情 = Rk结果单码详情类()
        if self.__isIniSoft == False:
            result_单码详情.错误编码 = -2
            result_单码详情.错误消息 = self.__GetErrorMsg(-2)
            lockdetail.release()
            return result_单码详情
        if self.__isLogin == False or self.__currentLoginCardOrAccount == "" or self.__loginToken == "":
            result_单码详情.错误编码 = -4
            result_单码详情.错误消息 = self.__GetErrorMsg(-4)
            lockdetail.release()
            return result_单码详情

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnum": self.__currentLoginCardOrAccount,
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.cardDetail)
        result_单码详情.错误编码 = RepResult.code
        result_单码详情.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            result_单码详情.到期时间 = jsonData["endtime"]
            result_单码详情.剩余点数 = int(jsonData["surpluspointvalue"])
            result_单码详情.备注 = jsonData["remarks"]
            result_单码详情.开通的价格类名称 = jsonData["pricename"]
            result_单码详情.开通的价格类型ID = jsonData["priceid"]
            if int(jsonData["openstate"]) == 1:
                result_单码详情.是否已开通 = True
            if int(jsonData["activestate"]) == 1:
                result_单码详情.是否已激活 = True
            result_单码详情.机器码 = jsonData["maccode"]
            result_单码详情.终端用户的qq = jsonData["qq"]
            result_单码详情.终端用户的微信 = jsonData["wx"]
            result_单码详情.终端用户的手机号 = jsonData["tel"]
            result_单码详情.终端用户的支付宝 = jsonData["alipay"]
            result_单码详情.终端用户的邮箱 = jsonData["email"]

        lockdetail.release()
        return result_单码详情

    def 账号登录函数(self, rk需要登录的账号: str, rk需要登录的密码: str) -> Rk结果账号登录类:
        lockLogin.acquire()
        result_账号登录 = Rk结果账号登录类()
        if self.__isIniSoft == False:
            result_账号登录.错误编码 = -2
            result_账号登录.错误消息 = self.__GetErrorMsg(-2)
            lockLogin.release()
            return result_账号登录
        if self.__isLogin:
            result_账号登录.错误编码 = -7
            result_账号登录.错误消息 = self.__GetErrorMsg(-7)
            lockLogin.release()
            return result_账号登录
        if rk需要登录的账号.strip() == "" or rk需要登录的密码.strip() == "":
            result_账号登录.错误编码 = -6
            result_账号登录.错误消息 = self.__GetErrorMsg(-6)
            lockLogin.release()
            return result_账号登录
        if len(self.__LoginList) > 0:
            for loginItem in self.__LoginList:
                if loginItem == rk需要登录的账号.strip():
                    result_账号登录.错误编码 = -8
                    result_账号登录.错误消息 = self.__GetErrorMsg(-8, rk需要登录的账号.strip())
                    lockLogin.release()
                    return result_账号登录
            time.sleep(2)

        if self.初始化软件结果属性.软件信息.单台设备最大登录数量 == 1:
            if len(self.__LoginList) == 0:
                token = self.__getToken(rk需要登录的账号.strip())
                if token != "":
                    timestamp = int(round(time.time() * 1000))
                    send_data = {
                        "cardnumorusername": rk需要登录的账号.strip(),
                        "maccode": self.__maccode,
                        "token": token,
                        "timestamp": timestamp
                    }
                    self.__GetRequestResult(send_data, BusinessType.loginOut)

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "username": rk需要登录的账号.strip(),
            "userpwd": rk需要登录的密码.strip(),
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.accountLogin)
        result_账号登录.错误编码 = RepResult.code
        result_账号登录.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            self.__isLogin = True
            self.__loginToken = jsonData["token"]
            self.__heartbeatKey = jsonData["heartbeatkey"]

            result_账号登录.备注 = jsonData["remarks"]
            result_账号登录.角色ID = jsonData["roleid"]
            result_账号登录.角色名称 = jsonData["rolename"]
            result_账号登录.终端客户的qq = jsonData["qq"]
            result_账号登录.终端客户的微信 = jsonData["wx"]
            result_账号登录.终端客户的邮箱 = jsonData["email"]
            result_账号登录.终端客户的支付宝 = jsonData["alipay"]
            result_账号登录.终端客户的手机号 = jsonData["tel"]
            result_账号登录.开通的价格类型ID = jsonData["priceid"]
            result_账号登录.到期时间 = jsonData["endtime"]
            result_账号登录.剩余点数 = jsonData["surpluspointvalue"]
            result_账号登录.开通的价格类型名称 = jsonData["pricename"]

            self.__currentLoginCardOrAccount = rk需要登录的账号
            self.__currentLoginPwd = rk需要登录的密码
            self.__LoginList.append(self.__currentLoginCardOrAccount)
            self.__saveToken(rk需要登录的账号.strip(), self.__loginToken)

            self.__heartbeatThread = threading.Thread(target=self.__heartbeat)
            self.__heartbeatThread.setDaemon(True)
            self.__heartbeatThread.start()

        lockLogin.release()
        return result_账号登录

    def 账号详情函数(self) -> Rk结果账号详情类:
        lockdetail.acquire()
        result_账号详情 = Rk结果账号详情类()
        if self.__isIniSoft == False:
            result_账号详情.错误编码 = -2
            result_账号详情.错误消息 = self.__GetErrorMsg(-2)
            lockdetail.release()
            return result_账号详情
        if self.__isLogin == False or self.__currentLoginCardOrAccount == "" or self.__loginToken == "":
            result_账号详情.错误编码 = -4
            result_账号详情.错误消息 = self.__GetErrorMsg(-4)
            lockdetail.release()
            return result_账号详情

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "username": self.__currentLoginCardOrAccount,
            "userpwd": self.__currentLoginPwd,
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.accountDetail)
        result_账号详情.错误编码 = RepResult.code
        result_账号详情.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            result_账号详情.到期时间 = jsonData["endtime"]
            result_账号详情.剩余点数 = int(jsonData["surpluspointvalue"])
            result_账号详情.备注 = jsonData["remarks"]
            result_账号详情.开通的价格类名称 = jsonData["pricename"]
            result_账号详情.开通的价格类型ID = jsonData["priceid"]
            if int(jsonData["openstate"]) == 1:
                result_账号详情.是否已开通 = True
            if int(jsonData["activestate"]) == 1:
                result_账号详情.是否已激活 = True
            result_账号详情.机器码 = jsonData["maccode"]
            result_账号详情.终端用户的qq = jsonData["qq"]
            result_账号详情.终端用户的微信 = jsonData["wx"]
            result_账号详情.终端用户的手机号 = jsonData["tel"]
            result_账号详情.终端用户的支付宝 = jsonData["alipay"]
            result_账号详情.终端用户的邮箱 = jsonData["email"]

        lockdetail.release()
        return result_账号详情

    def 账号注册函数(self, rk注册的账号: str, rk注册的密码: str) -> Rk结果基础类:
        lockregaccount.acquire()
        result_注册账号 = Rk结果基础类()
        if self.__isIniSoft == False:
            result_注册账号.错误编码 = -2
            result_注册账号.错误消息 = self.__GetErrorMsg(-2)
            lockregaccount.release()
            return result_注册账号
        if rk注册的账号.strip() == "" or rk注册的密码.strip() == "":
            result_注册账号.错误编码 = -10
            result_注册账号.错误消息 = self.__GetErrorMsg(-10)
            lockregaccount.release()
            return result_注册账号
        if len(rk注册的账号) > 15 or len(rk注册的密码) > 15:
            result_注册账号.错误编码 = -11
            result_注册账号.错误消息 = self.__GetErrorMsg(-11)
            lockregaccount.release()
            return result_注册账号

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "username": rk注册的账号.strip(),
            "userpwd": rk注册的密码.strip(),
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.accountRegister)
        result_注册账号.错误编码 = RepResult.code
        result_注册账号.错误消息 = RepResult.msg

        lockregaccount.release()
        return result_注册账号

    def 修改账号密码函数(self, rk账号: str, rk旧密码: str, rk新密码: str) -> Rk结果基础类:
        lockupdaccount.acquire()
        result_修改账号密码 = Rk结果基础类()
        if self.__isIniSoft == False:
            result_修改账号密码.错误编码 = -2
            result_修改账号密码.错误消息 = self.__GetErrorMsg(-2)
            lockupdaccount.release()
            return result_修改账号密码
        if rk账号.strip() == "" or rk旧密码.strip() == "" or rk新密码 == "":
            result_修改账号密码.错误编码 = -12
            result_修改账号密码.错误消息 = self.__GetErrorMsg(-12)
            lockupdaccount.release()
            result_修改账号密码
        if len(rk账号.strip()) > 15 or len(rk旧密码.strip()) > 15 or len(rk新密码.strip()) > 15:
            result_修改账号密码.错误编码 = -13
            result_修改账号密码.错误消息 = self.__GetErrorMsg(-13)
            lockupdaccount.release()
            result_修改账号密码

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "username": rk账号.strip(),
            "userpwd": rk旧密码.strip(),
            "newpwd": rk新密码.strip(),
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.updPwd)
        result_修改账号密码.错误编码 = RepResult.code
        result_修改账号密码.错误消息 = RepResult.msg

        lockupdaccount.release()
        return result_修改账号密码

    def 充值卡充值函数(self, rk被充值的卡密或账号: str, rk充值卡号: str) -> Rk结果基础类:
        lockrech.acquire()
        result_充值 = Rk结果基础类()
        if self.__isIniSoft == False:
            result_充值.错误编码 = -2
            result_充值.错误消息 = self.__GetErrorMsg(-2)
            lockrech.release()
            return result_充值
        if rk被充值的卡密或账号.strip() == "" or rk充值卡号.strip() == "":
            msg = "单码或账号"
            if self.初始化软件结果属性.软件信息.登录方式 == "卡密登录方式":
                msg = "单码"
            elif self.初始化软件结果属性.软件信息.登录方式 == "账号密码登录方式":
                msg = "账号"
            result_充值.错误编码 = -14
            result_充值.错误消息 = self.__GetErrorMsg(-14, msg)
            lockrech.release()
            return result_充值

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "rechcardnum": rk充值卡号.strip(),
            "cardnumorusername": rk被充值的卡密或账号.strip(),
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.rechCardRenewCardOrAccount)
        result_充值.错误编码 = RepResult.code
        result_充值.错误消息 = RepResult.msg

        lockrech.release()
        return result_充值

    def 充值卡详情函数(self, rk查询的充值卡: str) -> Rk结果充值卡详情类:
        lockrechdetail.acquire()
        result_充值卡详情 = Rk结果充值卡详情类()
        if self.__isIniSoft == False:
            result_充值卡详情.错误编码 = -2
            result_充值卡详情.错误消息 = self.__GetErrorMsg(-2)
            lockrechdetail.release()
            return result_充值卡详情
        if rk查询的充值卡.strip() == "":
            result_充值卡详情.错误编码 = -15
            result_充值卡详情.错误消息 = self.__GetErrorMsg(-15)
            lockrechdetail.release()
            return result_充值卡详情

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "rechcardnum": rk查询的充值卡.strip(),
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.rechCardNumDetail)
        result_充值卡详情.错误编码 = RepResult.code
        result_充值卡详情.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            result_充值卡详情.使用状态 = jsonData["rechcardstatename"]
            result_充值卡详情.消耗类型 = jsonData["consumetypename"]
            result_充值卡详情.所属软件 = jsonData["consumevaluename"]
            result_充值卡详情.可使用值 = jsonData["softname"]

        lockrechdetail.release()
        return result_充值卡详情

    def 扣点函数(self, rk扣的点数: int) -> Rk结果扣点类:
        lockpoint.acquire()
        result_扣点 = Rk结果扣点类()
        if self.__isIniSoft == False:
            result_扣点.错误编码 = -2
            result_扣点.错误消息 = self.__GetErrorMsg(-2)
            lockpoint.release()
            return result_扣点
        if self.__isLogin == False or self.__currentLoginCardOrAccount == "" or self.__loginToken == "":
            result_扣点.错误编码 = -4
            result_扣点.错误消息 = self.__GetErrorMsg(-4)
            lockpoint.release()
            return result_扣点
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnumorusername": self.__currentLoginCardOrAccount,
            "bucklevalue": rk扣的点数,
            "maccode": self.__maccode,
            "token": self.__loginToken,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.bucklePoint)
        result_扣点.错误编码 = RepResult.code
        result_扣点.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            result_扣点.剩余点数 = int(jsonData["surpluspointvalue"])

        lockpoint.release()
        return result_扣点

    def 修改备注函数(self, rk备注内容: str) -> Rk结果基础类:
        lockremarks.acquire()
        result_修改备注 = Rk结果基础类()
        if self.__isIniSoft == False:
            result_修改备注.错误编码 = -2
            result_修改备注.错误消息 = self.__GetErrorMsg(-2)
            lockremarks.release()
            return result_修改备注
        if self.__isLogin == False or self.__currentLoginCardOrAccount == "" or self.__loginToken == "":
            result_修改备注.错误编码 = -4
            result_修改备注.错误消息 = self.__GetErrorMsg(-4)
            lockremarks.release()
            return result_修改备注
        if rk备注内容.strip() == "":
            result_修改备注.错误编码 = -16
            result_修改备注.错误消息 = self.__GetErrorMsg(-16)
            lockremarks.release()
            return result_修改备注
        if len(rk备注内容.strip()) > 500:
            result_修改备注.错误编码 = -17
            result_修改备注.错误消息 = self.__GetErrorMsg(-17)
            lockremarks.release()
            return result_修改备注
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnumorusername": self.__currentLoginCardOrAccount,
            "remarks": rk备注内容.strip(),
            "maccode": self.__maccode,
            "token": self.__loginToken,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.updRemark)
        result_修改备注.错误编码 = RepResult.code
        result_修改备注.错误消息 = RepResult.msg

        lockremarks.release()
        return result_修改备注

    def 解绑机器码函数(self, rk需要解绑的卡密或账号: str) -> Rk结果解绑机器码类:
        lockunbundmac.acquire()
        result_解绑机器码 = Rk结果解绑机器码类()
        if self.__isIniSoft == False:
            result_解绑机器码.错误编码 = -2
            result_解绑机器码.错误消息 = self.__GetErrorMsg(-2)
            lockunbundmac.release()
            return result_解绑机器码
        if rk需要解绑的卡密或账号.strip() == "":
            msg = "单码或账号"
            if self.初始化软件结果属性.软件信息.登录方式 == "卡密登录方式":
                msg = "单码"
            elif self.初始化软件结果属性.软件信息.登录方式 == "账号密码登录方式":
                msg = "账号"
            result_解绑机器码.错误编码 = -18
            result_解绑机器码.错误消息 = self.__GetErrorMsg(-18, msg)
            lockunbundmac.release()
            return result_解绑机器码

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnumorusername": rk需要解绑的卡密或账号.strip(),
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.unbundMac)
        result_解绑机器码.错误编码 = RepResult.code
        result_解绑机器码.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            result_解绑机器码.到期时间 = jsonData["endtime"]
            result_解绑机器码.剩余点数 = int(jsonData["surpluspointvalue"])

        lockunbundmac.release()
        return result_解绑机器码

    def 获取远程变量函数(self, rk变量名: str) -> Rk结果获取远程变量类:
        lockgetvarvalue.acquire()
        result_获取远程变量 = Rk结果获取远程变量类()
        if self.__isIniSoft == False:
            result_获取远程变量.错误编码 = -2
            result_获取远程变量.错误消息 = self.__GetErrorMsg(-2)
            lockgetvarvalue.release()
            return result_获取远程变量
        if self.__isLogin == False or self.__currentLoginCardOrAccount == "" or self.__loginToken == "":
            result_获取远程变量.错误编码 = -4
            result_获取远程变量.错误消息 = self.__GetErrorMsg(-4)
            lockgetvarvalue.release()
            return result_获取远程变量
        if rk变量名.strip() == "":
            result_获取远程变量.错误编码 = -19
            result_获取远程变量.错误消息 = self.__GetErrorMsg(-19)
            lockgetvarvalue.release()
            return result_获取远程变量

        rkvarItem = None
        if len(self.__RkVarList) >0:
            for varItem in self.__RkVarList:
                if varItem.varname == rk变量名.strip():
                    rkvarItem = RkVar()
                    rkvarItem.变量值 = varItem.varvalue
                    break
        if rkvarItem!=None:
            result_获取远程变量.错误编码 = 0
            result_获取远程变量.错误消息="成功"
            result_获取远程变量.变量值 = rkvarItem.变量值
        else:
            timestamp = int(round(time.time() * 1000))
            send_data = {
                "cardnumorusername": self.__currentLoginCardOrAccount,
                "varname": rk变量名.strip(),
                "maccode": self.__maccode,
                "token": self.__loginToken,
                "timestamp": timestamp,
                "requestflag": str(timestamp)
            }
            RepResult = self.__GetRequestResult(send_data, BusinessType.getremoteVar)
            result_获取远程变量.错误编码 = RepResult.code
            result_获取远程变量.错误消息 = RepResult.msg
            if RepResult.code == 0:
                try:
                    jsonData = json.loads(RepResult.data)
                except:
                    jsonData = eval(RepResult.data)
                for varTemp in jsonData["varlist"]:
                    rkvarItem = RkVar()
                    rkvarItem.varname = varTemp["varname"]
                    rkvarItem.varvalue = varTemp["varvalue"]
                    self.__RkVarList.append(rkvarItem)
                    result_获取远程变量.变量值 = rkvarItem.varvalue
                    break

        lockgetvarvalue.release()
        return result_获取远程变量

    def 获取远程算法函数(self, rk算法ID: str,rk提交的参数:str) -> Rk结果获取远程算法类:
        lockgetcalvalue.acquire()
        result_获取获取远程算法 = Rk结果获取远程算法类()
        if self.__isIniSoft == False:
            result_获取获取远程算法.错误编码 = -2
            result_获取获取远程算法.错误消息 = self.__GetErrorMsg(-2)
            lockgetcalvalue.release()
            return result_获取获取远程算法
        if self.__isLogin == False or self.__currentLoginCardOrAccount == "" or self.__loginToken == "":
            result_获取获取远程算法.错误编码 = -4
            result_获取获取远程算法.错误消息 = self.__GetErrorMsg(-4)
            lockgetcalvalue.release()
            return result_获取获取远程算法
        if rk算法ID.strip() == "":
            result_获取获取远程算法.错误编码 = -20
            result_获取获取远程算法.错误消息 = self.__GetErrorMsg(-20)
            lockgetcalvalue.release()
            return result_获取获取远程算法
        if rk提交的参数.strip() == "":
            result_获取获取远程算法.错误编码 = -21
            result_获取获取远程算法.错误消息 = self.__GetErrorMsg(-21)
            lockgetcalvalue.release()
            return result_获取获取远程算法

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "maccode": self.__maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp),
            "token": self.__loginToken,
            "calculateid": rk算法ID.strip(),
            "requestargs": rk提交的参数.strip()
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.remoteCalculate)
        result_获取获取远程算法.错误编码 = RepResult.code
        result_获取获取远程算法.错误消息 = RepResult.msg
        if RepResult.code == 0:
            try:
                jsonData = json.loads(RepResult.data)
            except:
                jsonData = eval(RepResult.data)
            result_获取获取远程算法.服务器时间戳 = int(jsonData["servertimestamp"])
            result_获取获取远程算法.算法结果 = jsonData["calculateresult"]

        lockgetcalvalue.release()
        return result_获取获取远程算法

    def 禁用删除当前登录的单码或账号函数(self, rk禁用还是删除: Rk禁用还是删除枚举类) -> None:
        lockdisable.acquire()
        if self.__isIniSoft and self.__isLogin:
            timestamp = int(round(time.time() * 1000))
            send_data = {
                "cardnumorusername": self.__currentLoginCardOrAccount,
                "disablecardoraccounttype": rk禁用还是删除.value,
                "maccode": self.__maccode,
                "token": self.__loginToken,
                "timestamp": timestamp,
                "requestflag": str(timestamp)
            }
            RepResult = self.__GetRequestResult(send_data, BusinessType.disableCardOrAccount)

        lockdisable.release()

    def 退出登录函数(self) -> Rk结果基础类:
        lockloginout.acquire()
        result_退出登录 = Rk结果基础类()
        if self.__isIniSoft == False or self.__isLogin == False or self.__isLoginOut or self.__loginToken == "":
            result_退出登录.错误编码 = 0
            lockloginout.release()
            return result_退出登录

        self.__isStopHeartBeat = True
        print("等待心跳线程结束中...")
        waitNum = 0
        while self.__heartbeatThread.is_alive():
            time.sleep(1)
            waitNum = waitNum + 1
            if waitNum >= 5:
                terminator(self.__heartbeatThread)
        print("心跳线程已结束")

        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnumorusername": self.__currentLoginCardOrAccount,
            "maccode": self.__maccode,
            "token": self.__loginToken,
            "timestamp": timestamp
        }
        RepResult = self.__GetRequestResult(send_data, BusinessType.loginOut)
        result_退出登录.错误编码 = RepResult.code
        result_退出登录.错误消息 = RepResult.msg

        self.__clearLogin()
        self.__isLoginOut = True
        lockloginout.release()

        return result_退出登录

    def 获取瑞科验证SDK当前版本号(self)->str:
        result= "\n当前瑞科验证SDK版本：v3.0 瑞科官网：http://www.ruikeyz.com  http://rk2.ruikeyz.com  http://rk3.ruikeyz.com"
        print(result)
        return result
