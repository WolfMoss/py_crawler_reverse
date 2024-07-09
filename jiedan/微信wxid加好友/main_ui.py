# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(411, 531)
        icon = QIcon()
        icon.addFile(u"\u56fe\u6807.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(160, 500, 75, 23))
        self.pushButton.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.wxid_text = QTextEdit(Form)
        self.wxid_text.setObjectName(u"wxid_text")
        self.wxid_text.setGeometry(QRect(10, 150, 371, 301))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(140, 460, 151, 16))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 480, 351, 20))
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 0, 241, 41))
        self.label_4.setOpenExternalLinks(True)
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 100, 91, 16))
        self.km_text = QTextEdit(Form)
        self.km_text.setObjectName(u"km_text")
        self.km_text.setGeometry(QRect(80, 90, 301, 31))
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 130, 61, 16))
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 70, 411, 16))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.anzhuangButton = QPushButton(Form)
        self.anzhuangButton.setObjectName(u"anzhuangButton")
        self.anzhuangButton.setGeometry(QRect(10, 50, 181, 23))
        self.anzhuangButton.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.runButton = QPushButton(Form)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setGeometry(QRect(210, 50, 181, 23))
        self.runButton.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6781\u98ce\u52a0\u597d\u53cb\u5de5\u5177", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u542f\u52a8", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u591a\u4e2awxid\u7528\u56de\u8f66\u9694\u5f00", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u8f93\u5165wxid\u540e\uff0c\u70b9\u51fb\u542f\u52a8\uff0c\u7a0d\u7b49\u4e00\u4f1a\u5fae\u4fe1\u4f1a\u51fa\u73b0\u5bf9\u5e94\u7684\u5fae\u4fe1\u804a\u5929\u5bf9\u8bdd", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><a href=\"www.jixingwangluo.cn\"><span style=\" font-size:22pt; font-weight:700; text-decoration: underline; color:#29ccbc;\">\u70b9\u6211\u8bbf\u95ee\u6781\u98ce\u5b98\u7f51</span></a></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u2192\u8f93\u5165\u5361\u5bc6\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u2193\u8f93\u5165wxid\uff1a", None))
        self.anzhuangButton.setText(QCoreApplication.translate("Form", u"\u5b89\u88c5\u5b9a\u5236\u7248\u5fae\u4fe1\uff08\u9996\u6b21\u9700\u5b89\u88c5\uff09", None))
        self.runButton.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u5fae\u4fe1\uff08\u5fc5\u987b\u8fd0\u884c\u518d\u7528\u529f\u80fd\uff09", None))
    # retranslateUi

