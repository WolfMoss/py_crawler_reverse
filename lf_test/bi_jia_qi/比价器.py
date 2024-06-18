import requests
import execjs


jscode = open("jCryption111.js", "r", encoding="utf-8").read()
exec_js = execjs.compile(jscode)
kv = exec_js.call('getkey_value')

jCryptionKey=kv['jCryptionKey']
jCryptionValue=kv['jCryptionValue']

url = "https://www.bijiaqi.com/?action=user.login&_v=10.11194"
payload = f"jCryptionID=3196563126&jCryptionKey={jCryptionKey}&jCryptionValue={jCryptionValue}"
headers = {
  'Accept': '*/*',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie': 'CRID=bZxV0YwMUvawzynq; C_GAMEID=419; C_S_GAMEID=10; __root_domain_v=.bijiaqi.com; _qddaz=QD.986118723656079; _qdda=3-1.1; _qddab=3-ahj8n8.lxkjosnu; _clck=94t68h%7C2%7Cfmq%7C0%7C1630; _clsk=1a3lwha%7C1718724094864%7C2%7C1%7Cu.clarity.ms%2Fcollect',
  'Csrf-Token': '5TSfTR02Jc3VBg4xnqbJqXcfMLSF6umK',
  'Origin': 'https://www.bijiaqi.com',
  'Pragma': 'no-cache',
  'Referer': 'https://www.bijiaqi.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("POST", url, headers=headers, data=payload)

# 访问响应的 cookies
cookies = response.cookies

# 打印所有的cookie
for cookie in cookies:
    print(f"{cookie.name}: {cookie.value}")