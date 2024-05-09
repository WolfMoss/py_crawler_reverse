import os
import pickle

import requests
import base64
import json
import subprocess
import execjs


tjuser = 'wolfmoss'
tjpsw = 'Ilikecs123'

wxuserName = '15268317813'
wxpsw = 'ilikecs123'


#定义--------------------------------------
wxpassword='' #加密密码

session = requests.Session()
os.environ["NODE_PATH"] = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\node_modules"  # 这是node_modules在你系统中可能的位置，你需要根据你的系统环境来修改它

js_func = """
if (this.window === undefined) {
    this.window = this;
} 
var encryptFn = function(e) {
    const JSEncrypt = require('jsencrypt');
    var o = new JSEncrypt;
    o.setPublicKey("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDA5Zq6ZdH/RMSvC8WKhp5gj6Ue4Lqjo0Q2PnyGbSkTlYku0HtVzbh3S9F9oHbxeO55E8tEEQ5wj/+52VMLavcuwkDypG66N6c1z0Fo2HgxV3e0tqt1wyNtmbwg7ruIYmFM+dErIpTiLRDvOy+0vgPcBVDfSUHwUSgUtIkyC47UNQIDAQAB");
    return o.encrypt(e);
}
"""

headers = {
    'Connection': 'keep-alive',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'Connection': 'keep-alive',
  'Content-Length': '0',
  'Content-Type': 'application/json;charset=UTF-8',
  'Referer': 'https://user.wangxiao.cn/login',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
  'Cookie': 'sessionId=1715235191415'
}



# 一、图片文字类型(默认 3 数英混合)：
# 1 : 纯数字
# 1001：纯数字2
# 2 : 纯英文
# 1002：纯英文2
# 3 : 数英混合
# 1003：数英混合2
#  4 : 闪动GIF
# 7 : 无感学习(独家)
# 11 : 计算题
# 1005:  快速计算题
# 16 : 汉字
# 32 : 通用文字识别(证件、单据)
# 66:  问答题
# 49 :recaptcha图片识别
# 二、图片旋转角度类型：
# 29 :  旋转类型
#
# 三、图片坐标点选类型：
# 19 :  1个坐标
# 20 :  3个坐标
# 21 :  3 ~ 5个坐标
# 22 :  5 ~ 8个坐标
# 27 :  1 ~ 4个坐标
# 48 : 轨迹类型
#
# 四、缺口识别
# 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
# 33 : 单缺口识别（返回X轴坐标 只需要1张图）
# 五、拼图识别
# 53：拼图识别
def base64_api(uname, pwd, img, typeid):
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": img}
    ers = requests.post("http://api.ttshitu.com/predict", json=data)
    result = json.loads(ers.text)
    if result['success']:
        return result["data"]["result"]
    else:
        #！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]
    return ""

#----------------------------------------------------

#判断cookies.txt是否存在
if os.path.exists('cookies.txt'):

    print('cookies.txt文件存在')
    # 从本地文件加载cookies
    with open('cookies.txt', 'r') as fr:
        cookies = json.load(fr)
    # 更新session中的cookies
    session.cookies.update(cookies)
else:
    print('cookies.txt文件不存在')
    session.get("https://user.wangxiao.cn/login", headers=headers)
    res = session.post("https://user.wangxiao.cn/apis//common/getImageCaptcha", headers=headers)
    img = res.json()['data']
    print(img)
    timeres = session.post("https://user.wangxiao.cn/apis//common/getTime",headers=headers)
    time1 = timeres.json()['data']

    data_to_encrypt = wxpsw + '' + time1

    ctx = execjs.compile(js_func)
    wxpassword = ctx.call('encryptFn', data_to_encrypt)
    print(wxpassword)

    #image_data = base64.b64decode(img.replace('data:image/png;base64,', ''))
    imageCaptchaCode = base64_api(uname=tjuser, pwd=tjpsw, img=img.replace('data:image/png;base64,', ''), typeid=3)
    print(imageCaptchaCode)

    payload = {}
    payload['userName'] = wxuserName
    payload['password'] = wxpassword
    payload['imageCaptchaCode'] = imageCaptchaCode
    a= session.post("https://user.wangxiao.cn/apis//login/passwordLogin",headers=headers, data=json.dumps(payload))
    print(a.text)

    with open('cookies.txt', 'w') as fw:
        json.dump(session.cookies.get_dict(), fw)

payload = {}
payload['practiceType'] = '1'
payload['sign'] = 'jzs1'
payload['subsign'] = '5166078fbf1eed222fe9'
payload['day'] = '20240509'

#headers['Cookie']='pc_586760398_exam=jz1; mantis6894=b37380d16233493e8de6ba5dccd7ff3c@6894; safedog-flow-item=; autoLogin=null; userInfo=%7B%22userName%22%3A%22pc_586760398%22%2C%22token%22%3A%2282a251dd-1881-41ea-aa47-0860797d65e7%22%2C%22headImg%22%3Anull%2C%22nickName%22%3A%22152****7813%22%2C%22sign%22%3A%22fangchan%22%2C%22isBindingMobile%22%3A%221%22%2C%22isSubPa%22%3A%220%22%2C%22userNameCookies%22%3A%22fhGIZv00%2Fstr839jUmWTBw%3D%3D%22%2C%22passwordCookies%22%3A%22Xq8yT02ddqK7XDJmMojLtw%3D%3D%22%7D; token=82a251dd-1881-41ea-aa47-0860797d65e7; UserCookieName=pc_586760398; OldUsername2=fhGIZv00%2Fstr839jUmWTBw%3D%3D; OldUsername=fhGIZv00%2Fstr839jUmWTBw%3D%3D; OldPassword=Xq8yT02ddqK7XDJmMojLtw%3D%3D; UserCookieName_=pc_586760398; OldUsername2_=fhGIZv00%2Fstr839jUmWTBw%3D%3D; OldUsername_=fhGIZv00%2Fstr839jUmWTBw%3D%3D; OldPassword_=Xq8yT02ddqK7XDJmMojLtw%3D%3D; register-sign=jz1; sign=jz1',

questions_res= session.post("https://ks.wangxiao.cn/practice/listQuestions",headers=headers,  data=json.dumps(payload))
print(questions_res.json())