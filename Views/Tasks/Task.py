from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QStylePainter, QStyleOptionTab, QStyle


class Task(QTabWidget):

    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.name = 'Task'
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_campaign = QWidget()
        self.tab_task = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab_campaign, "Campaign")
        self.tabs.addTab(self.tab_task, "Task")

        # Create first tab
        self.tab_campaign.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab_campaign.layout.addWidget(self.pushButton1)
        self.tab_campaign.setLayout(self.tab_campaign.layout)

        # Add tabs to widget
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