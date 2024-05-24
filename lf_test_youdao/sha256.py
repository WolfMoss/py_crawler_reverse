import hashlib
import json
import time
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 #rsa加密有不同版本，加密出来不一样
import base64

key='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCZrdn8zDrN2wk0ey3fOy9Arisr5RbqT6bAda3rwtf8dz1XdjGpCp6BXtJIhgKR1Xj7/0gQwB/nykcR5Dycn5C/agXgxJoiBbYlaiYF70H748nPMzPAPt9vKC4y7lB3oQgst/MOmzdhzWSmH5elU89vzdleULyTvsQAHaS8vG7KLQIDAQAB'
key1='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCZrdn8zDrN2wk0ey3fOy9Arisr5RbqT6bAda3rwtf8dz1XdjGpCp6BXtJIhgKR1Xj7/0gQwB/nykcR5Dycn5C/agXgxJoiBbYlaiYF70H748nPMzPAPt9vKC4y7lB3oQgst/MOmzdhzWSmH5elU89vzdleULyTvsQAHaS8vG7KLQIDAQAB'
# public_key_pem = "-----BEGIN PUBLIC KEY-----\n" + \
#           textwrap.fill(key, 64) + \
#           "\n-----END PUBLIC KEY-----\n"

public_key_pem = "-----BEGIN PUBLIC KEY----- \n" + key + "\n-----END PUBLIC KEY-----"


def w():
    return str(uuid.uuid4())

random_uuid = w()
print(random_uuid)
# 获取当前13位时间戳（包含毫秒）
current_timestamp_ms = int(time.time() * 1000)
# 转换为10位时间戳（秒）
current_timestamp_s = current_timestamp_ms // 1000
print(current_timestamp_s)
salt = random_uuid.replace("-", "")

# 将公钥字符串转换为RSA密钥对象
public_key = RSA.import_key(public_key_pem)
# 创建一个PKCS1_OAEP模式的加密器
cipher_rsa = PKCS1_v1_5.new(public_key)
# 加密数据
encrypted_data = cipher_rsa.encrypt(salt.encode('utf-8'))
print("Encrypted data:", encrypted_data)
# 通常将加密后的数据转换为Base64字符串以便于传输和展示
encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')
print("Encrypted data (Base64):", encrypted_base64)

#c = a.encrypt(salt)
data = {
    "expire": current_timestamp_s,
    "params": [],
    "request": {
        "body": "{}",
        "content-type": "application/json"
    },
    "salt": salt
}
# 创建一个SHA256的hash对象
hash_object = hashlib.sha256()
# 将对象h转化为JSON字符串，然后计算其SHA256 hash值
hash_object.update(json.dumps(data,sort_keys=True, separators=(',', ':')).encode('utf-8'))
print(hash_object.hexdigest())