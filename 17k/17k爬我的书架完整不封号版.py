import os
import random
import time
import requests
from lxml import etree
from selenium import webdriver
import chardet

loginName = "你的账号"
password = "你的密码"
appkey = "每个人唯一的固定appkey"

driver = webdriver.Chrome()


class FileUtils:
    @staticmethod
    def mkdirs(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


headers = {
    'Accept': '*/*',
    'Referer': 'https://passport.17k.com/login/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                  'Safari/537.36',
}

session = requests.session()

# 第一次登录
logRes1 = session.post("https://passport.17k.com/ck/user/login", data={
    "loginName": loginName,
    "password": password
}, headers=headers)

driver.get("https://www.17k.com/")
for key, value in session.cookies.get_dict().items():
    driver.add_cookie({"name": key, "value": value})

try:
    driver.execute_script(logRes1.text)
except Exception as e:
    # 运行脚本后会出现 JavascriptException, 不用理会, cookie已经写入到driver中了
    print(e)

acw_sc__v2 = driver.get_cookie("acw_sc__v2")
guid = driver.get_cookie("GUID")
session.cookies.update({acw_sc__v2.get("name"): acw_sc__v2.get("value")})
session.cookies.update({guid.get("name"): guid.get("value")})

# 第二次登录
logRes2 = session.post("https://passport.17k.com/ck/user/login", data={
    "loginName": loginName,
    "password": password
}, headers=headers)

del headers["Referer"]

# 获取书架
res = session.get(f"https://user.17k.com/ck/author2/shelf?page=1&appKey={appkey}")

res.encoding = "utf8"
data = res.json().get("data")

list_bookid_name_mlhtml = []

# 遍历书架
for book in data:
    bookId = book['bookId']  # 书籍id
    bookName = book['bookName']  # 书籍名称
    bookMlListUrl = f"https://www.17k.com/list/{bookId}.html"
    bookMlListres = session.get(bookMlListUrl, headers=headers)
    bookMlListres.encoding = "utf8"
    print(f"bookId={bookId}；bookName={bookName}，目录获取成功")
    obj = {}
    obj['bookId'] = bookId
    obj['bookName'] = bookName
    obj['bookMlListresHtml'] = bookMlListres.text
    list_bookid_name_mlhtml.append(obj)

headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng," \
                    "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7 "
headers['Accept-Encoding'] = "gzip, deflate"
headers['Accept-Language'] = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"

# 获取每个卷下每个章节的url和名称
for obj in list_bookid_name_mlhtml:
    bookMlListresHtml = obj['bookMlListresHtml']
    tree = etree.HTML(bookMlListresHtml)
    VolumeHtmls = tree.xpath('//dl[@class="Volume"]')
    # 遍历卷
    for VolumeHtml in VolumeHtmls:
        VolumeNameHtml = VolumeHtml.xpath('.//span[@class="tit"]')[0]
        VolumeName = VolumeNameHtml.text  # 卷名称
        # 获取每个卷下的每个章节的url和名称
        ChapterHtmls = VolumeHtml.xpath('.//span[@class="ellipsis "]')
        hrefsHtmls = VolumeHtml.xpath('./dd/a')
        for ChapterHtml, hrefsHtml in zip(ChapterHtmls, hrefsHtmls):
            zjname = ChapterHtml.text.replace('\n', '').replace('\t', '')
            ChapterName = f"{VolumeName}_{zjname}"  # 卷_章节名称
            Chapterhref = f"https://www.17k.com{hrefsHtml.get('href')}"  # 章节url
            print(f"书名={obj['bookName']}；章节名称={ChapterName}；章节url={Chapterhref}")
            obj['Chapters'] = []
            obj['Chapters'].append({
                'ChapterName': ChapterName,
                'Chapterhref': Chapterhref
            })

            ChapterTextres = session.get(Chapterhref, headers=headers)
            encoding = chardet.detect(ChapterTextres.content)['encoding']
            ChapterTextres.encoding = encoding
            ChapterTextHtml = ChapterTextres.text
            tree = etree.HTML(ChapterTextHtml)
            #//div[@class="p"]//p
            content_list = tree.xpath('//div[@class="p"]//p/text()')
            output_dir = "./books/"
            FileUtils.mkdirs(folder_path=output_dir)
            output_file_path = os.path.join(output_dir, f"{obj['bookName']}.txt")
            with open(output_file_path, "a", encoding="utf-8") as fp:
                fp.write(ChapterName)
                fp.write("\n\n")
                for line in content_list:
                    fp.write(line)
                    fp.write("\n")
                fp.write("\n\n")
                print(f"{ChapterName}写入成功")

            sleep_time = random.uniform(3, 7)
            print(f"睡眠等待 {sleep_time} 秒, 防止被发现")
            time.sleep(sleep_time)
