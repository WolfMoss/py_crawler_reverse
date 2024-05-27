
from datetime import datetime
from ctypes import *
import time
#获取当前脚本所在目录
import os
cur_path = os.path.abspath(os.path.dirname(__file__))

print("Load DD!")
dll_path = os.path.join(cur_path, 'dd40605x64.dll')
dd_dll = windll.LoadLibrary(dll_path)
time.sleep(2)

st = dd_dll.DD_btn(0) #DD Initialize
if st==1:
    print("OK")
else:
    print("Error")
    exit(101)

print("当前时间（时:分:秒.毫秒）：", datetime.now().strftime("%H:%M:%S.%f"))
dd_dll.DD_key(302, 1)
dd_dll.DD_key(302, 2)
print("当前时间（时:分:秒.毫秒）：", datetime.now().strftime("%H:%M:%S.%f"))

print("Keyboard Left win")
#LWin is 601 in ddcode, 1=down, 2=up.
dd_dll.DD_key(601, 1)
dd_dll.DD_key(601, 2)
time.sleep(2)

print("Mouse move abs.")
dd_dll.DD_mov(200, 200)
time.sleep(2)

print("Mouse move rel.")
dd_dll.DD_movR(50, 50)
time.sleep(2)

print("Mouse Right button ")
#1==L.down, 2==L.up, 4==R.down, 8==R.up, 16==M.down, 32==M.up
dd_dll.DD_btn(4)
dd_dll.DD_btn(8)
time.sleep(2)







