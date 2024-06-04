import os
from win32com.client import Dispatch
import ctypes
import sys
import win32gui

def find_windows_with_title(title_text):
    def enum_windows_proc(hwnd, resultList):
        if win32gui.IsWindowVisible(hwnd) and title_text in win32gui.GetWindowText(hwnd):
            resultList.append(hwnd)
    window_list = []
    win32gui.EnumWindows(enum_windows_proc, window_list)
    return window_list

current_dir = os.path.dirname(os.path.abspath(__file__))
ARegJ = ctypes.windll.LoadLibrary(os.path.join(current_dir,'ARegJ64.dll'))
ARegJ.SetDllPathW(os.path.join(current_dir,'AoJia64.dll'), 0)
global AJ
AJ = Dispatch('AoJia.AoJiaD')
print(AJ.VerS())
AJ1 = Dispatch('AoJia.AoJiaD')


# 将'TITLE_TEXT'替换为您要搜索的标题文本
title_text = "chatgpt"
handles = find_windows_with_title(title_text)
for handle in handles:
    print(f"找到含有标题 '{title_text}' 的窗口句柄：{handle}")

Hwnd = handles[0]
print(Hwnd)
AJ.KQHouTai(Hwnd, 'DX', 'DX', 'DX', 'LAA|LAM|LFA|LFM', 3)
AJ.KeyPressS("F5")
AJ.MoveTo(100, 100)
AJ.RightClick()
AJ.GBHouTai()


title_text = "查窗口句柄工具"
handles = find_windows_with_title(title_text)
for handle in handles:
    print(f"找到含有标题 '{title_text}' 的窗口句柄：{handle}")
Hwnd = handles[0]
print(Hwnd)
AJ1.KQHouTai(Hwnd, 'DX', 'DX', 'DX', 'LAA|LAM|LFA|LFM', 3)
AJ1.KeyPressS("F5")
AJ1.MoveTo(100, 100)
AJ1.RightClick()
AJ1.GBHouTai()
