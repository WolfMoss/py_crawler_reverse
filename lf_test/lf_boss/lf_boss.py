import requests
import execjs
session = requests.Session()

url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=Java&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=1&pageSize=30"

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
  'x-requested-with': 'XMLHttpRequest'
}
response = session.request("GET", url, headers=headers, data=payload)
print(response.json())
name= response.json()['zpData']['name']
seed= response.json()['zpData']['seed']
ts= response.json()['zpData']['ts']

jscode = open("1.js", "r", encoding="utf-8").read()
exec_js = execjs.compile(jscode)

#zse96_md5 = exec_js.call('justmd5', pl_url, cookie_string)



url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=Java&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=1&pageSize=30"

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'cookie': '__zp_stoken__=0933fw4Zxw6APRAEOCA4GYk9RXn15wrZ4dGlHXsKEZVbCnEpBXEDColnDhcKYWsKLwqDCucK6wohnwoJpwr7Cu8O9wpfCrcKwwq5Lw7bCqsKWxJrDv8K7wr7DscKlwrPCpTA0CwAAAAx%2FfHx8cH98CQkVBxQUFAgGFRUVCUUuwpBmPDpEMy1OQUoNSV9TQ1hNAWVCTDMzZFcKADMmMzMzN8KxwrPCtwvCvsK4wrcLwrrCt8OECzM7NzjCs8O9JiHCuMOYBzUjwrjCpQfCsD0UwrPDqwfDh1ZnEMK7wrLCoy8xMcK3xLlEMB05OzA6MDwwMDAtPEXDg2VnHMKwwrbDnSA3GzgwMEVFMDAwOzs6LDBEXiIwMyc3AQgICQchRcK3Q8K4w5YwMA%3D%3D;expires=Wed, 29 May 2024 22:00:43 GMT;domain=.zhipin.com;path=/; __zp_sname__=4ae04288; __zp_sseed__=InZUA4w/K1dI3DRsaDIFu4ahiw70778MBINwD4YWBDU=; __zp_sts__=1716789687369',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
  'x-requested-with': 'XMLHttpRequest'
}

response = session.request("GET", url, headers=headers, data=payload)

print(response.text)
