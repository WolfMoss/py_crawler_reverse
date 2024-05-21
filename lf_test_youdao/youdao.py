import base64
import time
import hashlib
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

def dm516(input_data):
    # 你需要定义 T 函数的具体行为。
    hash_object = hashlib.md5()
    hash_object.update(input_data.encode('utf-8'))
    e_md51 = hash_object.hexdigest()
    return e_md51

def dm5bytes(input_data):
    # 你需要定义 T 函数的具体行为。
    hash_object = hashlib.md5()
    hash_object.update(input_data.encode('utf-8'))
    e_md51 = hash_object.digest()
    return e_md51

sjc = int(time.time() * 1000)
e = f"client=fanyideskweb&mysticTime={sjc}&product=webfanyi&key=fsdsogkndfokasodnaso"



# 获取16进制表示的摘要
e_md5 = dm516(e)
print(e_md5)
# 打印MD5摘要
print(len(e_md5))

url = "https://dict.youdao.com/webtranslate"

payload = {
    'i': '你好啊啊啊啊',
    'from': 'auto',
    'to': '',
    'useTerm': 'false',
    'domain': '0',
    'dictResult': 'true',
    'keyid': 'webfanyi',
    'sign': e_md5,
    'client': 'fanyideskweb',
    'product': 'webfanyi',
    'appVersion': '1.0.0',
    'vendor': 'web',
    'pointParam': 'client,mysticTime,product',
    'mysticTime': sjc,
    'keyfrom': 'fanyi.web',
    'mid': '1',
    'screen': '1',
    'model': '1',
    'network': 'wifi',
    'abtest': '0',
    'yduuid': 'abcdefg'
}

headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': '_ga=GA1.2.968003683.1711367817; OUTFOX_SEARCH_USER_ID_NCOO=990887343.5197785; OUTFOX_SEARCH_USER_ID=-816892489@101.83.227.151',
  'Origin': 'https://fanyi.youdao.com',
  'Referer': 'https://fanyi.youdao.com/',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

#ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl
#ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4

# 假设 T 是一个自定义的函数，用于处理密钥或IV，这里未定义其具体实现。


# 假设 't' 是密钥， 'o' 是 IV， 'e' 是待解密的经过base64编码的数据
# 需要将 't' 和 'o' 通过 T 函数处理后使用
key = dm5bytes('ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl')
iv = dm5bytes('ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4')

# 创建一个AES-CBC解密器实例
decryptor = Cipher(
    algorithms.AES(key),
    modes.CBC(iv),
    backend=default_backend()
).decryptor()

# 解密
# 假设 response.text 是 base64 编码的数据，需要先解码
data = response.text
encoded_data = base64.b64decode(data.encode(),altchars=b'-_')
decrypted_data = decryptor.update(encoded_data) + decryptor.finalize()

# 假设解密后的数据是utf-8编码的字符串，需要解码
decrypted_message = decrypted_data.decode('utf-8')

# 返回解密后的消息
print(decrypted_message)