import json
import requests
import random
import hashlib


def sha1_hash(msg: str) -> str:
  # Ensure the message is encoded in UTF-8
  msg = msg.encode('utf-8')

  # Create a hashlib sha1 object
  sha1 = hashlib.sha1()

  # Update the hashlib object with the message
  sha1.update(msg)

  # Get the hexadecimal digest of the hash
  hash_hex = sha1.hexdigest()

  return hash_hex




url = f"https://www.doyo.cn/User/Passport/token?username=hxy19931129&random={random.random()}"

payload = {}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Cookie': 'PHPSESSID=ggm5hbavaijdggbtsfjb3lnh15; doyo_www_uv_mark=true; Hm_lvt_b0affa74a0ef00f793803b2ae8a25f8a=1719052060; Hm_lpvt_b0affa74a0ef00f793803b2ae8a25f8a=1719052309',
  'Pragma': 'no-cache',
  'Referer': 'https://www.doyo.cn/passport/login?next=https://www.doyo.cn/game/85.html',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("GET", url, headers=headers, data=payload)

nonce = json.loads(response.text)['nonce']
ts = json.loads(response.text)['ts']


passwordsha1="f6eb772d4751beb5322aefc14447d186e2da1aaa"
password_jm_cs=nonce+str(ts)+passwordsha1
password=""

password = sha1_hash(password_jm_cs)
print("SHA-1 Hash:", password)

url = "https://www.doyo.cn/User/Passport/login"

payload = f"username=hxy19931129&password={password}&remberme=1&next=aHR0cHMlM0ElMkYlMkZ3d3cuZG95by5jbiUyRmdhbWUlMkY4NS5odG1s"
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie': 'PHPSESSID=ggm5hbavaijdggbtsfjb3lnh15; doyo_www_uv_mark=true; Hm_lvt_b0affa74a0ef00f793803b2ae8a25f8a=1719052060; Hm_lpvt_b0affa74a0ef00f793803b2ae8a25f8a=1719052309',
  'Origin': 'https://www.doyo.cn',
  'Pragma': 'no-cache',
  'Referer': 'https://www.doyo.cn/passport/login?next=https://www.doyo.cn/game/85.html',
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

print(response.text)
