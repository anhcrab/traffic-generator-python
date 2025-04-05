from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QStylePainter, QStyleOptionTab, QStyle
from PyQt5.QtCore import QRect, QPoint
from Views.Campaigns.List import List


class Campaign(QTabWidget):

    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.name = 'Campaign'

        self.tabs = QTabWidget()

        self.list = List(self)
        self.tabs.addTab(self.list, self.list.name)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.rect().center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()