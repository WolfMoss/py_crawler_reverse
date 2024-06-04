#免注册调用方法
import ctypes
import os
from comtypes.client import CreateObject
import win32com.client
# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前目录添加到DLL搜索路径
os.add_dll_directory(current_dir)

try:
    dm = win32com.client.Dispatch('dm.dmsoft')
    print('本机系统中已经安装大漠插件，版本为:', dm.ver())
except:
    print('本机并未安装大漠，正在免注册调用')
    dms = ctypes.windll.LoadLibrary('DmReg.dll')
    location_dmreg = os.getcwd()+'\dm.dll'
    dms.SetDllPathW(location_dmreg, 0)
    dm = CreateObject('dm.dmsoft')
    print('免注册调用成功 版本号为:',dm.Ver())
