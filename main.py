import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui

from view import MainView


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Traffic Generator - Terus'
        self.setWindowTitle(self.title)

        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 200
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.view = MainView(self)
        self.setCentralWidget(self.view)

        self.show()
        self.setWindowIcon(QtGui.QIcon('icon.png'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())