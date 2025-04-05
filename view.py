import threading

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QPushButton

from service import UserAgent, Proxy, Traffic, Client
from Storage.Storage import get_all_user_agents, get_all_proxies, get_all_traffic_urls, get_all_internal_links


class MainView(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.top_layout = QHBoxLayout()
        self.bot_layout = QHBoxLayout()
        self.run_traffic_button = QPushButton('Run Traffic')
        self.stop_traffic_button = QPushButton('Stop Traffic')
        self.run_traffic_button.clicked.connect(self.on_start_traffic)
        self.stop_traffic_button.clicked.connect(self.on_stop_traffic)
        self.bot_layout.addWidget(self.run_traffic_button)
        self.bot_layout.addWidget(self.stop_traffic_button)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bot_layout)
        self.setLayout(self.main_layout)

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
        direct_traffics = []
        search_traffics = []
        for web in webs:
            mobile = False
            if web['mobile'] is not None:
                mobile = web['mobile']
            traffic = Traffic(web['id'], web['url'], mobile, web["type"], web['required_qty'], web['current_qty'])
            traffic.set_keyword(web['keyword'])
            traffic.set_internal_links(self.__internal_links)
            if traffic.get_type() == 'Search':
                search_traffics.append(traffic)
            else:
                direct_traffics.append(traffic)
        for i in range(0, 5):
            client = Client("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            # client.set_user_agents(self.__user_agents)
            # client.log("Added user-agents")
            # client.set_proxies(self.__proxies)
            # client.log("Added proxies")
            self.__clients.append(client)
            client.setup_driver()
        for i in range(0, 5):
            if i < 5:
                self.__clients[i].set_traffics(search_traffics)
            else:
                self.__clients[i].set_traffics(direct_traffics)
        for client in self.__clients:
            thread = threading.Thread(target=self.work, args=(client,))
            thread.start()
            self.__threads.append(thread)

    def on_stop_traffic(self):
        for client in self.__clients:
            client.stop()
        for thread in self.__threads:
            thread.join()

    def work(self, client: Client):
        client.start()