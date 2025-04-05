import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QProxyStyle, QStyle
from PyQt5 import QtGui

from Service import UserAgent, Proxy
from Storage.Storage import get_all_user_agents
from Views.MainView import MainView


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Traffic Generator - Terus'
        self.left = 1400
        self.top = 30
        self.width = 400
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.view = MainView(self)
        self.setCentralWidget(self.view)

        self.show()
        self.setWindowIcon(QtGui.QIcon('icon.png'))


# class ProxyStyle(QProxyStyle):
#     def drawControl(self, element, option, painter, widget = ...):
#         if element == QStyle.CE_TabBarTabLabel:
#             r = QRect(option.rect)
#             w = 0
#             r.setHeight(option.fontMetrics.width(option.text) + w)
#             r.moveBottom(option.rect.bottom())
#             option.rect = r
#         QProxyStyle.drawControl(self, element, option, painter, widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle(ProxyStyle())
    ex = App()
    sys.exit(app.exec_())