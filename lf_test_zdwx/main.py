import os
from lxml import etree
from urllib.parse import urlparse, parse_qs
import requests
import json
import execjs

#配置--------------------------------------
tjuser = '图鉴用户名'
tjpsw = '图鉴密码'

wxuserName = '网校用户名'
wxpsw = '网校密码'
#-----------------------------------------

#定义--------------------------------------
datas=[]
wxpassword='' #加密密码
cok = {}
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
        cok = json.load(fr)
    # 更新session中的cookies
    session.cookies.update(cok)
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
    res = session.post("https://user.wangxiao.cn/apis//login/passwordLogin",headers=headers, data=json.dumps(payload))
    rescks= res.json()['data']
    print(rescks)

    cok['wxLoginUrl'] = "https://ks.wangxiao.cn/"
    cok['autoLogin'] = "null"
    cok['token'] = rescks['token']
    cok['UserCookieName'] = rescks['userName']
    cok['UserCookieName_'] = rescks['userName']
    cok['OldUsername2'] = rescks['userNameCookies']
    cok['OldUsername'] = rescks['userNameCookies']
    cok['OldUsername2_'] = rescks['userNameCookies']
    cok['OldUsername_'] = rescks['userNameCookies']
    cok['OldPassword'] = rescks['passwordCookies']
    cok['OldPassword_'] = rescks['passwordCookies']

    with open('cookies.txt', 'w') as fw:
        json.dump(cok, fw)

session.get("https://ks.wangxiao.cn/", headers=headers)
headers['Cookie']='; '.join([f'{k}={v}' for k, v in cok.items()])

#随便请求一个界面测试是否登录成功
payload = {}
payload['practiceType'] = '1'
payload['sign'] = 'jzs1'
payload['subsign'] = '5166078fbf1eed222fe9'
payload['day'] = '20240509'

questions_res= session.post("https://ks.wangxiao.cn/practice/listQuestions",headers=headers,  data=json.dumps(payload))
try:
    print(questions_res.json())
except:
    print('登录失败，可能ck过期，删除cookies.txt重新运行')

#获取所有科目
subjects_res= session.get("https://ks.wangxiao.cn/",headers=headers)
subjects_res.encoding='utf-8'
subjects_res_html=subjects_res.content
tree = etree.HTML(subjects_res_html)
subjects_html = tree.xpath("//a[starts-with(@href, '/TestPaper/list?sign=')]")

for subject_html in subjects_html:
    subject={}
    datas.append(subject)
    subject['subject_name'] = subject_html.xpath("./text()")[0]
    subject['subject_sign'] = subject_html.xpath("./@href")[0].split('=')[1]
    print(subject['subject_name'], subject['subject_sign'])
    #https://ks.wangxiao.cn/practice/listEveryday?sign=jzs1
    subject['subject_url']= 'https://ks.wangxiao.cn/practice/listEveryday?sign='+subject['subject_sign']


for subject in datas:
    subject['everdays'] = []
    listEveryday_res = session.get(subject['subject_url'],headers=headers)
    listEveryday_res.encoding = 'utf-8'
    tree = etree.HTML(listEveryday_res.content)
    listEveryday_htmls = tree.xpath("//*[@class='test-item']")
    for listEveryday_html in listEveryday_htmls:
        sjobj = {}
        subject['everdays'].append(sjobj)
        #https://ks.wangxiao.cn/practice/getQuestion?practiceType=1&sign=jzs1&subsign=5166078fbf1eed222fe9&day=20240509
        everdays_url="https://ks.wangxiao.cn"+ listEveryday_html.xpath('.//li')[3].xpath('.//a/@href')[0]
        sjobj['everdays_url']=everdays_url
        sjobj['questions'] = []
        print(sjobj['everdays_url'])

        # 使用urlparse()函数解析URL
        parsed_url = urlparse(everdays_url)
        # 使用parse_qs()函数解析出URL中的参数
        params = parse_qs(parsed_url.query)

        payload = {}
        payload['practiceType'] = params['practiceType'][0]
        payload['sign'] = params['sign'][0]
        payload['subsign'] = params['subsign'][0]
        payload['day'] = params['day'][0]
        print(payload)
        questions_res = session.post("https://ks.wangxiao.cn/practice/listQuestions", headers=headers,
                                     data=json.dumps(payload))
        sjobj['sj_title'] = questions_res.json()['title']
        questions_datas = questions_res.json()['Data'][0]['questions']
        for questions_data in questions_datas:
            question={}
            sjobj['questions'].append(question)
            question['question_text']=questions_data['content']
            print(sjobj['sj_title'],question['question_text'])
            question['options']=[]
            for option in questions_data['options']:
                option_obj={}
                option_obj['name']=option['name']
                option_obj['content']=option['content']
                question['options'].append(option_obj)

print(datas)