import threading

import openpyxl
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

from Service import Client, Traffic, UserAgent, Proxy
from Storage.Storage import get_all_user_agents, get_all_proxies, get_all_traffic_urls, get_all_internal_links


def work(clients):
    for client in clients:
        client.start()


class List(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.name = 'List'
        self.layout = QHBoxLayout(self)
        self.run_traffic_button = QPushButton('Run Traffic')
        self.stop_traffic_button = QPushButton('Stop Traffic')
        self.run_traffic_button.clicked.connect(self.on_start_traffic)
        self.stop_traffic_button.clicked.connect(self.on_stop_traffic)
        self.layout.addWidget(self.run_traffic_button)
        self.layout.addWidget(self.stop_traffic_button)
        self.setLayout(self.layout)

        self.__user_agents = []
        for item in get_all_user_agents():
            self.__user_agents.append(UserAgent(item["id"], item["value"], item["device_type"], item["device_name"]))
        self.__proxies = []
        for item in get_all_proxies():
            self.__proxies.append(Proxy(
                item['id'],
                item["ip"],
                item["port"],
                item["code"],
                item["country"],
                item["anonymity"],
                item["allow"],
                item["google"],
                item["https"]
            ))
        self.__traffic_urls = get_all_traffic_urls()
        self.__internal_links = get_all_internal_links()
        self.__threads = []
        self.__clients = []

    def on_start_traffic(self):
        webs = get_all_traffic_urls()
        for i in range(0, 1):
            client = Client("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            traffics = []
            for web in webs:
                mobile = False
                if web['mobile'] is not None:
                    mobile = web['mobile']
                traffic = Traffic(web['id'], web['url'], mobile, web["type"], web['required_qty'], web['current_qty'])
                traffic.set_keyword(web['keyword'])
                traffic.set_internal_links(self.__internal_links)
                traffics.append(traffic)
            client.set_traffics(traffics)
            client.log("Added traffics")
            # client.set_user_agents(self.__user_agents)
            # client.log("Added user-agents")
            # client.set_proxies(self.__proxies)
            # client.log("Added proxies")
            self.__clients.append(client)
            client.setup_driver()
        for client in self.__clients:
            thread = threading.Thread(target=self.work, args=(client,))
            thread.start()
            self.__threads.append(thread)

    def on_stop_traffic(self):
        for client in self.__clients:
            client.join()
            client.stop()

    def work(self, client: Client):
        client.start()