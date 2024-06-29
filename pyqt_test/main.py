import json

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTextBrowser, QPushButton
from main_ui import Ui_Form

with open('config.json', 'r') as f:
    try:
        config = json.load(f)
    except:
        config={}
        print("配置文件未读到")

class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化 UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        if len(config)>0:
            self.ui.Minutes_text.setText(config['Minutes'])
            self.ui.dailiurl_text.setText(config['dailiurl'])
            self.ui.km_text.setText(config['km'])

        # 获取UI文件中的小部件对象

        # 连接信号和槽
        self.ui.pushButton.clicked.connect(lambda:self.pushButton_click("Hello, World!"))



    # 函数
    def pushButton_click(self, text):
        print(text)
        print(self.ui.Minutes_text.toPlainText())
        print(self.ui.dailiurl_text.toPlainText())
        print(self.ui.km_text.toPlainText())

        config['Minutes']=self.ui.Minutes_text.toPlainText()
        config['dailiurl'] = self.ui.dailiurl_text.toPlainText()
        config['km'] = self.ui.km_text.toPlainText()

        with open('config.json', 'w') as file:
            json.dump(config, file)

if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MyMainWindow()
    mainWindow.show()
    app.exec()