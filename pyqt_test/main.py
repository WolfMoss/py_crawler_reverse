import random
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = [
            "Hallo Welt",
            "浣犲ソ锛屼笘鐣�",
            "Hei maailma",
            "Hola Mundo",
            "袩褉懈胁械褌 屑懈褉",
        ]

        self.button = QPushButton("Click me!")
        self.message = QLabel("Hello World")
        self.message.alignment = Qt.AlignCenter

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.button)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        self.message.text = random.choice(self.hello)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())