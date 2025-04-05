import json
import random
import time
import uuid

import selenium_stealth
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver import ActionChains, Keys, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType

from Storage.Storage import set_traffic_url, set_proxy, get_traffic_url


class UserAgent:
    __id: int
    __value: str
    __device_type: str
    __device_name: str

    def __init__(self, ua_id: int, value: str, device_type: str, device_name: str):
        self.__id = ua_id
        self.__value = value
        self.__device_type = device_type
        self.__device_name = device_name

    def get_id(self):
        return self.__id

    def set_id(self, ua_id: int):
        self.__id = ua_id

    def get_value(self):
        return self.__value

    def set_value(self, value: str):
        self.__value = value

    def get_device_type(self):
        return self.__device_type

    def set_device_type(self, device_type: str):
        self.__device_type = device_type

    def get_device_name(self):
        return self.__device_name

    def set_device_name(self, device_name: str):
        self.__device_name = device_name


class Proxy:
    __id: int
    __ip_address: str
    __port: int
    __code: str
    __country: str
    __anonymity: str
    __is_allowed: bool
    __is_google: bool
    __is_https: bool

    def __init__(self, proxy_id: int, ip_address: str, port: int, code: str = None, country: str = None, anonymity: str = None, is_allowed: bool = True, is_google: bool = True, is_https: bool = True):
        self.__id = proxy_id
        self.__ip_address = ip_address
        self.__port = port
        self.__code = code
        self.__country = country
        self.__anonymity = anonymity
        self.__is_allowed = is_allowed
        self.__is_google = is_google
        self.__is_https = is_https

    def get_id(self):
        return self.__id

    def set_id(self, proxy_id: int):
        self.__id = proxy_id

    def get_ip_address(self):
        return self.__ip_address

    def set_ip_address(self, ip_address: str):
        self.__ip_address = ip_address

    def get_port(self):
        return self.__port

    def set_port(self, port: int):
        self.__port = port

    def is_allowed(self):
        return self.__is_allowed

    def set_allowed(self, is_allowed: bool):
        self.__is_allowed = is_allowed
        if self.__is_allowed:
            set_proxy(self.__id, 'allow', 'yes')
        else:
            set_proxy(self.__id, 'allow', 'no')

    def is_google(self):
        return self.__is_google

    def set_google(self, is_google: bool):
        self.__is_google = is_google
        if self.__is_google:
            set_proxy(self.__id, 'google', 'yes')
        else:
            set_proxy(self.__id, 'google', 'no')

    def is_https(self):
        return self.__is_https

    def set_https(self, is_https: bool):
        self.__is_https = is_https
        if self.__is_https:
            set_proxy(self.__id, 'https', 'yes')
        else:
            set_proxy(self.__id, 'http', 'no')


class Traffic:
    __id: int
    __url: str
    __client_id: str
    __ip_address: str
    __is_google_recaptcha: bool
    __is_mobile: bool
    __type: str
    __keyword: str
    __rank: int
    __internal_links: list[str]
    __required_qty: int
    __current_qty: int

    def __init__(self, traffic_id: int, url: str, is_mobile: bool, traffic_type: str, required_qty: int, current_qty: int):
        self.__id = traffic_id
        self.__url = url
        self.__is_mobile = is_mobile
        self.__type = traffic_type
        self.__required_qty = required_qty
        self.__current_qty = current_qty

    def get_id(self):
        return self.__id

    def set_id(self, traffic_id: int):
        self.__id = traffic_id

    def get_url(self):
        return self.__url

    def set_url(self, url: str):
        self.__url = url

    def is_mobile(self):
        return self.__is_mobile

    def set_mobile(self, is_mobile: bool):
        self.__is_mobile = is_mobile

    def get_keyword(self):
        return self.__keyword

    def set_keyword(self, keyword: str):
        self.__keyword = keyword

    def get_rank(self):
        return self.__rank

    def set_rank(self, rank: int):
        self.__rank = rank

    def get_client_id(self):
        return self.__client_id

    def set_client_id(self, client_id):
        self.__client_id = client_id

    def get_ip_address(self):
        return self.__ip_address

    def set_ip_address(self, ip_address: str):
        self.__ip_address = ip_address

    def get_is_google_recaptcha(self):
        return self.__is_google_recaptcha

    def set_is_google_recaptcha(self, is_google_recaptcha: bool):
        self.__is_google_recaptcha = is_google_recaptcha

    def get_type(self):
        return self.__type

    def set_type(self, traffic_type: str):
        self.__type = traffic_type

    def get_required_qty(self):
        return self.__required_qty

    def set_required_qty(self, required_qty: int):
        self.__required_qty = required_qty

    def get_current_qty(self):
        return self.__current_qty

    def set_current_qty(self, current_qty: int):
        self.__current_qty = current_qty
        set_traffic_url(self.__id, 'current_qty', str(self.__current_qty))

    def add_current_qty(self):
        self.__current_qty = int(get_traffic_url(self.__id)['current_qty'])
        self.__current_qty += 1
        set_traffic_url(self.__id, 'current_qty', self.__current_qty)

    def get_internal_links(self):
        return self.__internal_links

    def set_internal_links(self, internal_links: list[str]):
        self.__internal_links = internal_links

    def log(self, message: str):
        print("Traffic", self.__type, "Event:", message)


class Client:
    __id: str
    __driver: webdriver.Chrome
    __ip_addresses: list[str]
    __os_version: str
    __proxies: list[Proxy] = []
    __user_agents: list[UserAgent] = []
    __languages: list[str] = ['vi-vn', 'vi']
    __exe_file_location: str
    __traffics = []
    __options: webdriver.ChromeOptions
    __done_automated_software_captcha: bool = False
    __current_proxy: Proxy

    def __init__(self, exe_file_location: str, client_id: str = None):
        self.__exe_file_location = exe_file_location
        if client_id is None:
            self.__id = str(uuid.uuid4())
        else:
            self.__id = client_id
        self.log("Init")

    def get_id(self):
        return self.__id

    def get_driver(self):
        return self.__driver

    def get_ip_addresses(self):
        return self.__ip_addresses

    def set_ip_addresses(self, ip_addresses: list[str]):
        self.__ip_addresses = ip_addresses

    def get_os_version(self):
        return self.__os_version

    def set_os_version(self, os_version: str):
        self.__os_version = os_version

    def get_proxies(self):
        return self.__proxies

    def set_proxies(self, proxies: list[Proxy]):
        self.__proxies = proxies
        self.log("Added proxies")

    def get_user_agents(self):
        return self.__user_agents

    def set_user_agents(self, user_agents: list[UserAgent]):
        self.__user_agents = user_agents
        self.log("Added user-agents")

    def get_languages(self):
        return self.__languages

    def set_languages(self, languages: list[str]):
        self.__languages = languages

    def get_traffics(self):
        return self.__traffics

    def set_traffics(self, traffics: list[Traffic]):
        self.__traffics = traffics
        self.log("Added Traffic")

    def setup_driver(self):
        self.log("Setting up driver...")
        # d = DesiredCapabilities.CHROME
        # d['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument('--disable-blink-features=AutomationControlled')
        self.__options.add_argument('--disable-popup-blocking')
        self.__options.add_argument('--no-sandbox')
        self.__options.add_argument('--disable-dev-shm-usage')
        self.__options.add_experimental_option("useAutomationExtension", False)
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')
        if len(self.__user_agents) > 0:
            ua = random.choice(self.__user_agents)
            while ua.get_device_type() != "desktop":
                ua = random.choice(self.__user_agents)
        seleniumwire_options = {
            'proxy': {
                'http': 'http://yiekd_phanp:HsRDWj87@117.0.200.23:40599',
                'https': 'https://yiekd_phanp:HsRDWj87@117.0.200.23:40599',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        if len(self.__proxies) > 0:
            proxy = random.choice(self.__proxies)
            while not proxy.is_google():
                proxy = random.choice(self.__proxies)
            self.log(f"Chose proxy {proxy.get_id()} - {proxy.get_ip_address()}:{proxy.get_port()}")
            # seleniumwire_options = {
            #     'proxy': {
            #         'https': f'https://{proxy.get_ip_address()}:{proxy.get_port()}',
            #         'no_proxy': 'localhost,127.0.0.1'
            #     }
            # }
            self.__current_proxy = proxy
        self.__options.binary_location = self.__exe_file_location
        self.set_driver(webdriver.Chrome(options=self.__options, seleniumwire_options=seleniumwire_options))
        self.__driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        if self.__languages is not None:
            selenium_stealth.stealth(
                driver=self.__driver,
                languages=self.__languages,
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fullscreen=True,
                run_on_insecure_origins=False,
                fix_hairline=True
            )
        else:
            selenium_stealth.stealth(
                driver=self.__driver,
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fullscreen=True,
                run_on_insecure_origins=False,
                fix_hairline=True
            )
        self.log("Created driver")

    def set_driver(self, driver: webdriver.Chrome):
        self.__driver = driver

    def start(self):
        self.log("Starting...")
        while True:
            for traffic in self.get_traffics():
                # curr = int(traffic.get_current_qty()) if traffic.get_current_qty().isDigit() else 0
                # req = int(traffic.get_required_qty()) if traffic.get_required_qty().isDigit() else 0
                if traffic.get_current_qty() < int(traffic.get_required_qty()):
                    self.generate_traffic(traffic)

    def stop(self):
        self.__driver.quit()
        self.log("Stopped")

    def generate_traffic(self, traffic: Traffic):
        if traffic.get_type() == 'Search':
            traffic.log("Started")
            self.__generate_traffic_search(traffic)
        else:
            self.__generate_traffic_direct(traffic)

    def __generate_traffic_direct(self, traffic: Traffic):
        self.__driver.get(traffic.get_url())
        # while self.get_status() not in [200, 201, 202, 301, 302]:
        #     new_proxy = random.choice(self.__proxies)
        #     self.__driver.proxy = { "https": f"https://{new_proxy.get_ip_address()}:{new_proxy.get_port()}" }
        #     self.__driver.get(traffic.get_url())
        self.handle_scroll(traffic)
        self.handle_internal_links(traffic)

    def __generate_traffic_search(self, traffic: Traffic):
        self.__driver.get("https://www.google.com")
        # while self.get_status() not in [200, 201, 202, 301, 302] and len(self.__proxies) > 0:
        #     new_proxy = random.choice(self.__proxies)
        #     self.__driver.proxy = { "https": f"https://{new_proxy.get_ip_address()}:{new_proxy.get_port()}" }
        #     self.__driver.get("https://www.google.com")
        time.sleep(2)
        if self.handle_search(traffic):
            self.handle_scroll(traffic)
            self.handle_internal_links(traffic)

    def handle_scroll(self, traffic: Traffic):
        traffic.log("Scrolling the page...")
        height = int(self.__driver.execute_script("return document.documentElement.scrollHeight"))
        y = 0
        step = int(height / 30)
        for timer in range(0, 30):
            self.__driver.execute_script(f"window.scrollTo(0, {str(y)})")
            time.sleep(2)
            y += step

    def handle_internal_links(self, traffic: Traffic):
        action = ActionChains(self.__driver)
        print(traffic.get_internal_links())
        for internal_link in traffic.get_internal_links():
            try:
                target_internal = self.__driver.find_element(By.CSS_SELECTOR, f".footer-link[href='{internal_link}']")
                traffic.log(f"Internal links - {internal_link}")
                action.click(target_internal).perform()
                self.handle_scroll(traffic)
            except Exception as e:
                traffic.log(f"Internal links - {e}")
        traffic.add_current_qty()

    def handle_search(self, traffic: Traffic):
        action = ActionChains(self.__driver)
        traffic.log("Searching...")
        time.sleep(3)
        search_box = self.__driver.find_elements(By.CSS_SELECTOR, "textarea")
        if len(search_box) == 0:
            search_box = self.__driver.find_elements(By.CSS_SELECTOR, "input:is([name='q']):not([type='hidden'])")
        if len(search_box) > 0:
            action.click(search_box[0]).pause(1).send_keys(traffic.get_keyword()).pause(2).send_keys(Keys.ENTER).pause(3).perform()
            is_captcha = self.handle_recaptcha(traffic)
            if traffic.is_mobile():
                while len(self.__driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Kết quả tìm kiếm khác']")) == 0:
                    time.sleep(1)
                show_more = self.__driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Kết quả tìm kiếm khác']")
                target_elements = self.__driver.find_elements(By.CSS_SELECTOR, f"a[href='{traffic.get_url()}'] div[role='heading']")
                while target_elements == 0 and show_more[0].get_attribute('style') != 'display: none;':
                    action.pause(0.5).scroll_to_element(show_more[0]).perform()
                    action.pause(1).click(show_more[0]).perform()
                    show_more = self.__driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Kết quả tìm kiếm khác']")
                    target_elements = self.__driver.find_elements(By.CSS_SELECTOR, f"a[href='{traffic.get_url()}'] div[role='heading']")
            else:
                while len(self.__driver.find_elements(By.CSS_SELECTOR, "#botstuff")) == 0:
                    time.sleep(1)
                current_page = 1
                target_elements = self.__driver.find_elements(By.CSS_SELECTOR, f"a[href='{traffic.get_url()}'] h3")
                while len(target_elements) == 0 and current_page < 5:
                    current_page += 1
                    next_page = self.__driver.find_element(By.CSS_SELECTOR, f"#botstuff table a[aria-label='Page {current_page}']")
                    action.scroll_to_element(next_page).pause(1).click(next_page).perform()
                    target_elements = self.__driver.find_elements(By.CSS_SELECTOR, f"a[href='{traffic.get_url()}'] h3")
                if len(target_elements) == 0:
                    return False
                action.scroll_to_element(target_elements[0]).pause(0.5).click(target_elements[0]).perform()
                return True
        return False

    def handle_recaptcha(self, traffic: Traffic):
        action = ActionChains(self.__driver)
        recaptcha = self.__driver.find_elements(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
        if len(recaptcha) != 0 and not self.__done_automated_software_captcha:
            action.click(recaptcha[0]).pause(2).perform()
            self.__done_automated_software_captcha = True
            return True
        while len(recaptcha) != 0 and self.__done_automated_software_captcha:
            # new_proxy = random.choice(self.__proxies)
            # self.__driver.proxy = {
            #     "https": f"https://{new_proxy.get_ip_address()}:{new_proxy.get_port()}" ,
            # }
            self.__driver.get("https://www.google.com")
            self.handle_search(traffic)
        traffic.log(f"Recaptcha not found")
        return False

    def get_status(self):
        status = self.__driver.execute_script("return window.performance.getEntries().find(e => e.entryType === 'navigation').responseStatus")
        return status
        # logs = self.__driver.get_log('performance')
        # for log in logs:
        #     if log['message']:
        #         d = json.loads(log['message'])
        #         try:
        #             content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
        #             response_received = d['message']['method'] == 'Network.responseReceived'
        #             self.log(d['message'])
        #             if content_type and response_received:
        #                 return d['message']['params']['response']['status']
        #             else:
        #                 return d['message']['params']['response']
        #         except:
        #             return 500

    def log(self, message: str):
        print("Client", self.__id, "-", message)


# if __name__ == "__main__":
#     webs = [
#         {
#             "url": "https://terusvn.com/seo-copywriting-la-gi/",
#             "keyword": "seo copywriting terusvn.com"
#         },
#         {
#             "url": "https://terusvn.com/viet-chu-in-dam-tren-facebook/",
#             "keyword": "chữ in đậm",
#         },
#         {
#             "url": "https://terusvn.com/internet-la-gi/",
#             "keyword": "internet",
#         },
#         {
#             "url": "https://terusvn.com/infographic-la-gi/",
#             "keyword": "infographic",
#         },
#         {
#             "url": "https://terusvn.com/mo-hinh-b2e-la-gi/",
#             "keyword": "b2e",
#         },
#         {
#             "url": "https://terusvn.com/kol-la-gi/",
#             "keyword": "kol là gì",
#         },
#         {
#             "url": "https://terusvn.com/voucher-coupon-va-ma-giam-gia-la-gi/",
#             "keyword": "voucher",
#         }, {
#             "url": "https://terusvn.com/cms-la-gi/",
#             "keyword": "cms",
#         },
#         {
#             "url": "https://terusvn.com/mmo-la-gi-nhung-dieu-ma-ban-can-biet/",
#             "keyword": "mmo là gì",
#         },
#         {
#             "url": "https://terusvn.com/mo-hinh-waterfall-la-gi/",
#             "keyword": "waterfall",
#         },
#         {
#             "url": "https://terusvn.com/hashtag-la-gi/",
#             "keyword": "hashtag",
#         },
#         {
#             "url": "https://terusvn.com/ceo-la-gi/",
#             "keyword": "ceo là gì",
#         },
#         {
#             "url": "https://terusvn.com/content-la-gi-kien-thuc-va-cach-xay-dung-content/",
#             "keyword": "content là gì",
#         },
#         {
#             "url": "https://terusvn.com/swot-la-gi-cach-xay-dung-mo-hinh-swot/",
#             "keyword": "swot",
#         },
#         {
#             "url": "https://terusvn.com/phan-mem-seo/",
#             "keyword": "phần mềm seo miễn phí",
#         },
#         {
#             "url": "https://terusvn.com/phan-mem-seo/",
#             "keyword": "phần mềm seo tốt nhất",
#         },
#         {
#             "url": "https://terusvn.com/phan-mem-fake-ip-cho-website/",
#             "keyword": "fake ip",
#         },
#         {
#             "url": "https://terusvn.com/visual-basic-la-gi/",
#             "keyword": "vb",
#         },
#         {
#             "url": "https://terusvn.com/phan-mem-seo/",
#             "keyword": "phần mềm seo chuyên nghiệp",
#         },
#         {
#             "url": "https://terusvn.com/cach-giam-dung-luong-anh/",
#             "keyword": "giảm dung lượng ảnh",
#         },
#         {
#             "url": "https://terusvn.com/marketing-4p-la-gi-va-dieu-can-biet/",
#             "keyword": "4p",
#         },
#         {
#             "url": "https://terusvn.com/target-la-gi/",
#             "keyword": "target la gì",
#         },
#         {
#             "url": "https://terusvn.com/concept-la-gi/",
#             "keyword": "concept là gì",
#         },
#         {
#             "url": "https://terusvn.com/agency-la-gi/",
#             "keyword": "agency là gì",
#         },
#         {
#             "url": "https://terusvn.com/seeding-la-gi-tim-hieu-ve-seeding/",
#             "keyword": "seeding là gì",
#         },
#         {
#             "url": "https://terusvn.com/marketing-tool/",
#             "keyword": "marketing tools",
#         },
#         {
#             "url": "https://terusvn.com/phan-mem-seo/",
#             "keyword": "công cụ seo",
#         },
#         {
#             "url": "https://terusvn.com/workshop/",
#             "keyword": "workshop",
#         }
#     ]
#     client = Client("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
#     client.setup_driver()
#     traffics = []
#     for i in range(1, len(webs)):
#         traffics.append(Traffic(i, webs[i]['url'], False, "Direct"))
#     client.set_traffics(traffics)
#     client.start()
#