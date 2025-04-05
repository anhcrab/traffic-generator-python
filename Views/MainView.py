from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from Views.Campaigns.Campaign import Campaign
from Views.Tasks.Task import Task


class MainView(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)

        self.Campaign = Campaign(self)
        self.tabs.addTab(self.Campaign, self.Campaign.name)
        self.Task = Task(self)
        self.tabs.addTab(self.Task, self.Task.name)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)