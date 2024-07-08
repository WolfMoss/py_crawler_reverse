import json
import requests
from PySide6.QtWidgets import QApplication,QSystemTrayIcon, QWidget, QMessageBox, QMainWindow, QTextBrowser, QPushButton
from PySide6.QtGui import QIcon
from main_ui import Ui_Form
import ctypes
user32 = ctypes.windll.user32
import win32con
import pyhont对接瑞科验证示例



def enum_windows():
  EnumWindows = user32.EnumWindows
  EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                       ctypes.POINTER(ctypes.c_int),
                                       ctypes.POINTER(ctypes.c_int))
  GetWindowText = user32.GetWindowTextW
  GetWindowTextLength = user32.GetWindowTextLengthW
  IsWindowVisible = user32.IsWindowVisible
  windows = []
  def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
      length = GetWindowTextLength(hwnd)
      buf = ctypes.create_unicode_buffer(length + 1)
      GetWindowText(hwnd, buf, length + 1)
      windows.append((hwnd, buf.value))
    return True

  EnumWindows(EnumWindowsProc(foreach_window), 0)
  return windows

def get_window_handle(partial_title):
  windows = enum_windows()
  for hwnd, title in windows:
    if partial_title.lower() in title.lower():
      return hwnd
  return None

def hide_window(hwnd):
    # SW_HIDE: 0 - Hide the window
    ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_HIDE)

    # 设置窗口样式，使其透明和不可见
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, win32con.GWL_EXSTYLE)
    ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW
    ctypes.windll.user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE, ex_style)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA)

class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("tb.ico"))
        # 设置任务栏图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("tb.ico"))
        # 初始化 UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 获取UI文件中的小部件对象

        # 连接信号和槽
        self.ui.pushButton.clicked.connect(lambda:self.pushButton_click("Hello, World!"))



    # 函数
    def pushButton_click(self, text):
        km = str(self.ui.km_text.toPlainText())
        if not km:
            QMessageBox.information(self, "信息", "请输入卡密。")
            return

        rest = pyhont对接瑞科验证示例.单码操作示例(km)
        if rest == 0:
            QMessageBox.information(self, "信息", "请输入正确的卡密。")
            return

        QMessageBox.information(self, "信息", "准备启动，点击ok后开始执行，耐心等待程序弹出执行结果。")

        wxids = str(self.ui.wxid_text.toPlainText()).splitlines()
        for wxid in wxids:
            try:
                if not wxid:
                    continue
                url = "http://localhost:7600/wcf/send_txt"

                payload = json.dumps({
                    "aters": [
                        "string"
                    ],
                    "msg": "你好",
                    "receiver": wxid
                })
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
            except Exception as e:
                print(e)
        QMessageBox.information(self, "信息", "启动完毕，所有wxid已发送完毕。")


if __name__ == '__main__':
    hwnd = get_window_handle('cmd.exe')
    hide_window(hwnd)


    app = QApplication([])
    mainWindow = MyMainWindow()
    mainWindow.show()
    app.exec()