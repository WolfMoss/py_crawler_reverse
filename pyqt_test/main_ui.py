# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(150, 260, 75, 23))
        self.pushButton.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Minutes_text = QTextEdit(Form)
        self.Minutes_text.setObjectName(u"Minutes_text")
        self.Minutes_text.setGeometry(QRect(90, 10, 241, 31))
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 71, 16))
        self.dailiurl_text = QTextEdit(Form)
        self.dailiurl_text.setObjectName(u"dailiurl_text")
        self.dailiurl_text.setGeometry(QRect(90, 60, 241, 31))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 71, 16))
        self.km_text = QTextEdit(Form)
        self.km_text.setObjectName(u"km_text")
        self.km_text.setGeometry(QRect(90, 110, 241, 31))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 120, 71, 16))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u542f\u52a8", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u51e0\u5206\u949f", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"IP\u63a5\u53e3", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"IP\u63a5\u53e3\u540d", None))
    # retranslateUi

