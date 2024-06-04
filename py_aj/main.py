import os
from win32com.client import Dispatch
import ctypes
import sys

# global base_path
# if getattr(sys, 'frozen', False):
#     base_path = sys._MEIPASS
# else:
#     base_path = os.path.abspath(os.path.dirname(__file__))

current_dir = os.path.dirname(os.path.abspath(__file__))
ARegJ = ctypes.windll.LoadLibrary(os.path.join(current_dir,'ARegJ64.dll'))
ARegJ.SetDllPathW(os.path.join(current_dir,'AoJia64.dll'), 0)
global AJ
global current_work_dir
AJ = Dispatch('AoJia.AoJiaD')
print(AJ.VerS())

Hwnd = AJ.FindWindow(0, "notepad.exe", 0, "", "记事本", 0, 0)
print(Hwnd)
AJ.KQHouTai(Hwnd, 'GDI1', 'KDI', 'WM', 'LS', 0)
AJD = AJ.MoveR(100, 100)
