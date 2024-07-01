import json
import traceback

import requests
from datetime import datetime, timedelta
import time
from fake_useragent import UserAgent
import asyncio
import aiohttp
import httpx
ua = UserAgent()
import yanzheng

kongzhi = 0

countobj = {"num":0}

with open('config.json', 'r') as f:
    config = json.load(f)

#yanzheng.method_name(config['km'])

class Client:
    # 初始化
    def __init__(self):
        self.timestamp = int(time.time() * 1000) * 1000  # 乘以1000仅为示例放大
        self.ua = ua.random
        self.n = ""
        self.answer = ""
        self.maths_key=""
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://poll.fm/',
            'user-agent': self.ua
        }
        self.proxies = None
        self.proxy = None

    async def get_n(self, session):
        url = f"https://poll.fm/n/dbac4123e8eba4b904d00f62e0a84a2d/13956837?{self.timestamp}"
        response = await session.get(url, headers=self.headers)
        return response.text

    async def get_answer(self, session):
        restext = await self.get_n(session)
        n = restext.split("'")[1]
        self.n = n
        #print(n)
        url = f"https://polls.polldaddy.com/vote-js.php?p=13956837&b=0&a=62214828,&o=&va=16&cookie=0&tags=13956837-src:poll-embed&n={n}&url=https%3A//poll.fm/13956837/embed"

        response = await session.get(url, headers=self.headers)
        ans_txt = response.text
        self.maths_key = ans_txt.split('value="')[1].split('"')[0]


        #print(self.maths_key)

        question_txt_arr = ans_txt.split("<span><p>")[1].split("=")[0].split("+")
        question_txt1 = int(question_txt_arr[0].strip())
        question_txt2 = int(question_txt_arr[1].strip())
        return question_txt1 + question_txt2

    async def do_voting(self,re=True):
        print(self.proxy,"开始投票")
        try:
            #con = aiohttp.TCPConnector(ssl=False)
            timeout = httpx.Timeout(5.0, connect=2.0)
            async with httpx.AsyncClient(proxies=self.proxies,timeout=timeout) as session:
                answer=await self.get_answer(session)
                url = f"https://polls.polldaddy.com/vote-js.php?p=13956837&b=0&a=62214828,&o=&va=16&cookie=0&tags=13956837-src:poll-embed&n={self.n}&url=https%3A//poll.fm/13956837/embed&maths=1&answer={answer}&maths_key={self.maths_key}"
                #print(url)
                response = await session.get(url, headers=self.headers)
                response_text = response.text
                if "Total Votes" in response_text:
                    countobj['num'] = countobj['num']+1
                    print(self.proxy,"投票结束")

                    if re == True:
                        for i in range(0, 4):
                            answer2 = await self.get_answer(session)
                            url = f"https://polls.polldaddy.com/vote-js.php?p=13956837&b=0&a=62214828,&o=&va=16&cookie=0&tags=13956837-src:poll-embed&n={self.n}&url=https%3A//poll.fm/13956837/embed&maths=1&answer={answer2}&maths_key={self.maths_key}"
                            # print(url)
                            response = await session.get(url, headers=self.headers)
                            response_text = response.text
                            if "Total Votes" in response_text:
                                countobj['num'] = countobj['num'] + 1
                                print(self.proxy, "投票结束")


        except Exception as e:
            #traceback.print_exc()
            print(self.proxy,e)


async def dotoupiao(proxies):
    client = Client()
    client.proxies=proxies
    client.proxy = client.proxies['http://']
    #client.proxy = client.proxies['http']
    await client.do_voting()

async def main():

    tasks = []
    dataips=[]
    for i in range(0, 1):
        try:
            print("获取IP",i)
            res = requests.get(config['dailiurl'])
            #dataips.extend(res.json()['proxies'])
            #print(res.json())
            dataips.extend(res.json()['data']['proxy_list'])

        except:
            print("获取IP失败,跳过",i)

    print(len(dataips))



    for proxy_info in dataips:

        proxiesip = proxy_info.split(':')[0]
        proxiesport = proxy_info.split(':')[1]

        proxies={}

        # proxiesip = proxy_info['ip']
        # proxiesport = proxy_info['port']

        # proxies['http'] = f'http://{proxiesip}:{proxiesport}'
        # proxies['https'] = f'http://{proxiesip}:{proxiesport}'

        proxies['http://'] = f'http://{proxiesip}:{proxiesport}'
        proxies['https://'] = f'http://{proxiesip}:{proxiesport}'

        #proxies['socks5'] = f'socks5://{proxiesip}:{proxiesport}'
        tasks.append(dotoupiao(proxies))

    await asyncio.gather(*tasks)

# print("开始投票...")
# # 获取当前时间
# start_time = datetime.now()
#
# # 循环持续10分钟
# if kongzhi == 1:
#     end_time = start_time + timedelta(minutes=1)
# else:
#     end_time = start_time + timedelta(minutes=int(config['Minutes']))
#
# while datetime.now() < end_time:
#     try:
#         asyncio.run(main())
#     except Exception as e:
#         traceback.print_exc()
#         time.sleep(0.5)
#         #print(e)
#
# print("投票完成，投了",countobj['num'])
# input("按任意键退出")

async def periodic_task():
    # 获取当前时间
    start_time = datetime.now()

    # 循环持续10分钟
    if kongzhi == 1:
        end_time = start_time + timedelta(minutes=1)
    else:
        end_time = start_time + timedelta(minutes=int(config['Minutes']))


    while datetime.now() < end_time:
        try:
            asyncio.create_task(main())
        except Exception as e:
            traceback.print_exc()

        await asyncio.sleep(2)

    print("投票完成")

if __name__ == '__main__':


    print("开始投票...")
    asyncio.run(periodic_task())
    print("投票完成，投了", countobj['num'])
    input("按任意键退出")