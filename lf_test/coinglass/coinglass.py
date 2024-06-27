import requests
import execjs




url = "https://capi.coinglass.com/api/home/v2/coinMarkets?sort=&order=&keyword=&pageNum=1&pageSize=20&ex=all"

payload = {}
headers = {
  'accept': 'application/json',
  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'cache-control': 'no-cache',
  'cache-ts': '1719471679289',
  'encryption': 'true',
  'language': 'zh',
  'origin': 'https://www.coinglass.com',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://www.coinglass.com/',
  'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.json())

wait_data = response.json()['data']
n='Y29pbmdsYXNzL2Fw'
headersuser=response.headers['User']

# 读取 JavaScript 文件
with open('coinglass.js', 'r', encoding='utf-8') as file:
    js_code = file.read()

# 创建 Node.js 运行时引擎上下文
ctx = execjs.get('Node').compile(js_code)

# 调用 JavaScript 函数并传递参数
result = ctx.call('jiemi', wait_data, headersuser,n)

print(result)  # 输出 JavaScript 方法的执行结果



