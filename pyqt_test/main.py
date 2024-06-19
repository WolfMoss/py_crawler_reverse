from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTextBrowser, QPushButton
from main_ui import Ui_Form


class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化 UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 获取UI文件中的小部件对象
        self.textEdit = self.ui.textEdit
        self.pushButton = self.ui.pushButton

        # 连接信号和槽
        self.pushButton.clicked.connect(lambda:self.pushButton_click("Hello, World!"))

    # 函数
    def pushButton_click(self, text):
        self.textEdit.setText(text)



if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MyMainWindow()
    mainWindow.show()
    app.exec()