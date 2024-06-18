import requests
import time
import random
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def replace(match):
    n = int(16 * random.random())
    if match == 'x':
        return hex(n)[2:]
    else:
        return hex(3 & n | 8)[2:]

template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
Nonce = ''.join([replace(e) if e in ('x', 'y') else e for e in template])
print("Nonce===",Nonce)


# 获取当前时间的时间戳（毫秒）
Timestamp = int(time.time() * 1000)
print("Timestamp===", Timestamp)

jmkey1= """
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCdgJNfUFPDNJsL
HObB1JMu7E1+nuwkFHmXnBU2AOM2dweE+tpmViZo90w+YQIuIS8MoVz60AGHbLE8
BYcdxQEKmPsqq0Lq/1ltIdp1YcO9W60qSxwpZS+7o73ljRrrtOXcE1UUpH5l07Fh
ziCIRDI/4ODCA8AJ1kV6IyfPNM2Fes3BEqhMOgw4Z5i4pZHnb4Nm+4kEXmyM+UgQ
cShcXZA/dx5MXKA2Bbb0I0G6HS3D4nMhnm6IgYWEyT8ngenMOyy+ysBuHWt2j9Cp
AGLWRyqHigFcKTlP5BSIkU+8sqssab1jvDg2F8MXWuupwF43OVARgHofiwQBAHPo
PfTfPlMvAgMBAAECggEBAJKQpZNasrfCak0LFgllgZl2uB6OUPy6OPRGgM6CQO3c
EhlDPp1gqdmf10ltCJRYuOmt91JG4kVddgh+tF+VhgSQm5n3SQxZlqQhjqMQ2Q+L
Ejd7Mberu6GHHB1TE6wn6IbFTrUo5Z5oQnbbVBa6L3CWGVEyIDCHPpwLvu3pGx+L
083dNQUiF8WcSGybl1h4ZapAGdndPYJReKYccNBYu5IzTEjtG3VpMHl56hD8fPV8
SStYv4sEffyCbze5/KvG3WlG+8n1WzBRMAN1U8Qk3JlMM/g5Y2tL1elI2pQRmjH8
EVxNUzB9Ob/qk2N6pF4KwhDWjILkHdoXilHMgP5x0gECgYEAy9O9ShtRNwXdFzHe
v+buyjvWWvwTVRUBehe8BWO1QaZ4c/INw1Ks4pgoKvXyU1DRx5OloIx6BWDbs00O
1W1cDue2I/Ymvx5Q/XJmZK4eR2U3a2dmKLKVhCXhJ3y02R/OZ2xQHV3NZXqz88kf
rEmEKYTW9q2gVsZa82XpQhKnBYECgYEAxdFJ55AkU7VfzpV1x68NUetomB3OWxyq
Cugn3STLNx7Jw6FaK3dwRz0eKIbwCRxtlluZmxWX0jWSvj3cyLRBIKTD8atUfJW2
+ESKZb/i961HhhQjXqNfGQpmMdEazNqv0sDzQ5jHHIjc63oty/FjckcC+AaDGZIJ
VGCet5J5kK8CgYBm2R/Bfgk792R5KLvaHz/MoebmoB1tKB1HqyQ/n/E9AC/1aWUS
cuwzpk1WaCXvbm98Af9oBJopjpctYSuj+/ugtcDNYo5oj3aUfJ44HTfAFM2jD1iY
HoydUrPKxf1HNepje17tgoB6vTCCSbEGsU3T2WjSrgei4ZHREVJi+aB3gQKBgEy8
rm2sxdrPHjZWVlU6+/DOYEm6LkW77d7DRkuMLWTZha1lF0SLVbvc4qkYB1+RbpWI
PSMjEj0SWTWBa/dTrXwLTpOeQez+avcOJ53m/RXVW0yQ3VOmDor5NMGYe0wCfXhF
L1kGmB7inMigIcnefxRipa0vYYX217WqsYdGw++zAoGBALKswyV5j1GjVjN+fS1t
N9R0x+S7cKBqW6Bwj6aAdo4+spmRn9WK4h9Zk2k7BMUiqJKTce6RdW0Ep+aTErRs
LL0sBHArhQdaQvq0yS57BJUZm3ASrOpp3wkQdDejS3YEKiIQSG2kNFRanh8RbtbA
ac7pfLikyQm795/qF0H9YHgF
-----END PRIVATE KEY-----
"""
jmkey2 = f'Timestamp&{Timestamp}&/byairport-flight/flight/list&{Nonce}&{"{"}"day":0,"depOrArr":"1","pageNum":1,"pageSize":15,"terminal":"","type":"1"{"}"}'

def load_private_key(private_key_str):
    private_key = serialization.load_pem_private_key(
        private_key_str.encode(),  # 私钥字符串编码为字节
        password=None,  # 如果私钥有密码，请提供
    )
    return private_key

def fe(e, n):
    private_key = e  # 假设 e 是私钥对象
    message = n.encode()  # 将消息转换为字节串

    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

private_key = load_private_key(jmkey1)
signature = fe(private_key, jmkey2)

# 将签名转换为base64字符串
signature_base64 = base64.b64encode(signature).decode('utf-8')

print("Signature===", signature_base64)

url = "https://www.baiyunairport.com/byairport-flight/flight/list"

payload = "{\"type\":\"1\",\"terminal\":\"\",\"day\":0,\"depOrArr\":\"1\",\"pageNum\":1,\"pageSize\":15}"
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json;charset=UTF-8',
  'Cookie': 'Hm_lvt_0effb2f651854e064f7d24a159e08bd5=1718729550; Hm_lpvt_0effb2f651854e064f7d24a159e08bd5=1718729550; Hm_lvt_e9e5e5ffd5a25d3f4d7e1466807ef7b7=1718729550; Hm_lpvt_e9e5e5ffd5a25d3f4d7e1466807ef7b7=1718729550; Hm_lvt_783519365e6df848bd882229527a15bc=1718729550; Hm_lpvt_783519365e6df848bd882229527a15bc=1718729550; Hm_lvt_483eff6efca2ca9bff48af354895a36f=1718729550; Hm_lpvt_483eff6efca2ca9bff48af354895a36f=1718729550; Hm_lvt_38ddcda5baa19a6a899f6f3f7471381a=1718729550; Hm_lpvt_38ddcda5baa19a6a899f6f3f7471381a=1718729550; JSESSIONID=RpYuWEdhiC_CMRfhbFXr7xUBi9tvJRSsANPdkZ4S',
  'Nonce': Nonce,
  'Origin': 'https://www.baiyunairport.com',
  'Pragma': 'no-cache',
  'Referer': 'https://www.baiyunairport.com/flight/dep',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Signature': signature_base64,
  'Timestamp': str(Timestamp),
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
  'locale': 'zh_CN',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
