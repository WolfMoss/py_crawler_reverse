import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# 自定义的处理函数
def en(hex_string):
    return hex_string  # 这里仅作为示例，实际上可能有其他处理

# AES解密函数
def decrypt_aes_ecb(t, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_data = base64.b64decode(t)
    decrypted_bytes = cipher.decrypt(decoded_data)
    try:
        decrypted_text = unpad(decrypted_bytes, AES.block_size, style='pkcs7').decode('utf-8')
    except ValueError:
        # 填充移除失败，返回解密的原始字节数据
        decrypted_text = decrypted_bytes.decode('utf-8').rstrip('\x02')
    return decrypted_text




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
n='6fb8d6f248074171'


# 假设密文（十六进制格式）和密钥
t = wait_data  # 加密的文本（十六进制格式）
e = n  # 秘钥

# 使用UTF-8编码解析密钥
key = e.encode('utf-8')

# 解密操作
decrypted_string = decrypt_aes_ecb(t, key)

# 调用自定义函数
n = en(decrypted_string)
print(n)  # 输出解密后的结果
