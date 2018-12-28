import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Deepthought'
        self.left = 500
        self.top = 500
        self.width = 480
        self.height = 480
        self.shutter = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.set_status("Status: OK")
        button = QPushButton('Toggle shutter', self)
        button.setToolTip('Epi shutter on/off')
        button.move(50, 30)
        button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        if not self.shutter:
            self.set_status("Shutter: ON")
            self.shutter = 1
        else:
            self.set_status("Shutter: OFF")
            self.shutter = 0

    def set_status(self, message):
        self.statusBar().showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
