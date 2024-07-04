import json
import threading
import traceback

import httpx



class Helper:
    def __init__(self):
        self.lock = threading.Lock()
        self.proxies = {}
        self.proxy_cycle = {'iterator': None}
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    async def getProxy(self):
        # 获取下一个代理
        try:
            if not self.proxy_cycle['iterator'] or next(self.proxy_cycle['iterator'], None) is None:
                self.proxy_cycle['iterator']=await self.get_proxy_dataips()
                print('换IP池')
            proxy_info = next(self.proxy_cycle['iterator'])
            #print(proxy_info)
            proxiesip = proxy_info['ip']
            proxiesport = proxy_info['port']
            self.proxies['http://'] = f'http://{proxiesip}:{proxiesport}'
            self.proxies['https://'] = f'http://{proxiesip}:{proxiesport}'

        except StopIteration:
            print('没有代理了')

    #获取代理池，全局唯一共享线程
    async def get_proxy_dataips(self):
        with self.lock:
            async with httpx.AsyncClient() as client:
                res = await client.get(self.config['dailiurl'])

            # UU代理
            # dataips=res.json()['proxies']

            #巨量代理
            proxy_list = res.json()['data']['proxy_list']
            dataips=[]
            for proxy_info in proxy_list:
                proxiesip = proxy_info.split(':')[0]
                proxiesport = proxy_info.split(':')[1]
                proxy_info={'ip':proxiesip,'port':proxiesport}
                dataips.append(proxy_info)



            # 使用itertools.cycle无限循环列表
            return iter(dataips)


    async def get_url_autoproxy(self,url,headers=None):
        try:
            if not self.proxies :
                await self.getProxy()
            async with httpx.AsyncClient(proxies=self.proxies) as client:
                response = await client.get(url, headers=headers)
                return response
        except Exception as e:
            #traceback.print_exc()
            print('换IP：', e,url)
            await self.getProxy()
            return await self.get_url_autoproxy(url,headers)

    async def post_url_autoproxy(self,url,headers=None,body={}):
        try:
            if not self.proxies :
                await self.getProxy()
            async with httpx.AsyncClient(proxies=self.proxies) as client:
                response = await client.post(url, headers=headers,body=body)
                return response
        except Exception as e:
            # print('换IP：', e,proxies,url)
            await self.getProxy()
            return await self.post_url_autoproxy(url,headers,body)