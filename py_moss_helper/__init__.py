import os
import threading
from lxml import etree
import requests

proxy_cycle = []

class Helper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.lock = threading.Lock()
        self.proxies = {}

    @staticmethod
    def getXpath(content,xpathtext):
        tree = etree.HTML(content)
        # 使用XPath表达式选择元素
        elements = tree.xpath(xpathtext)
        return elements

    @staticmethod
    def geturl_global_session(url,headers,session = requests.Session(),encoding='utf-8'):
        try:
            session.headers = headers
            response = session.get(url)
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求报错: {e}")
            return None
    @staticmethod
    def posturl_global_session(url,headers,params={},session = requests.Session(),encoding='utf-8'):
        try:
            session.headers = headers
            response = session.post(url,json=params)
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求报错: {e}")
            return None

    @staticmethod
    def mkdirs(self,folder_path):
        """
        创建指定路径的目录（如果该目录不存在）。
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    #输入文件夹路径和文件名，返回文件路径，如文件夹不存在则会创建
    @staticmethod
    def get_file_path(self,folder_path,file_name):
        self.mkdirs(folder_path)
        output_file_path = os.path.join(folder_path, f"{file_name}.txt")
        return output_file_path

    #返回当前脚本路径下的userdata文件夹绝对路径
    @staticmethod
    def get_userdata_path():
        # 获取当前代码文件所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接文件路径
        user_data_dir = os.path.join(current_dir, 'userdata')
        return  user_data_dir

    def getProxy(self,proxy_cycle):
        # 获取下一个代理
        try:
            if not proxy_cycle['iterator'] or next(proxy_cycle['iterator'], None) is None:
                proxy_cycle['iterator']=self.get_proxy_dataips(proxy_cycle)
                print('换IP池')
            proxy_info = next(proxy_cycle['iterator'])
            #print(proxy_info)
            proxiesip = proxy_info['ip']
            proxiesport = proxy_info['port']
            self.proxies['http'] = f'http://{proxiesip}:{proxiesport}'
            self.proxies['https'] = f'http://{proxiesip}:{proxiesport}'

        except StopIteration:
            print('没有代理了')


    def get_proxy_dataips(self):
        with self.lock:
            res = requests.get('http://uu-proxy.com/api/get_proxies?id=MLNXJZUSZ9&size=50&schemes=http,socks5&support_https=true&restime_within_ms=5000&format=json')

            dataips=res.json()['proxies']
            # 使用itertools.cycle无限循环列表

            return iter(dataips)


    def choose_func_getproxy(self,proxy_cycle):
        self.getProxy(proxy_cycle)

    def geturl_autoproxy(self,proxy_cycle,url,headers, session=requests.session()):
        try:
            session.headers = headers
            res = session.get(url, proxies=self.proxies)
            return res
        except Exception as e:
            # print('换IP：', e,proxies,url)
            self.choose_func_getproxy(proxy_cycle)
            return self.geturl(url, session, headers)

    def geturl_autoproxy(self,proxy_cycle,url,headers,body={}, session=requests.session()):
        try:
            session.headers = headers
            res = session.post(url, proxies=self.proxies,json=body)
            return res
        except Exception as e:
            # print('换IP：', e,proxies,url)
            self.choose_func_getproxy(proxy_cycle)
            return self.geturl_autoproxy(url, session, headers,body)