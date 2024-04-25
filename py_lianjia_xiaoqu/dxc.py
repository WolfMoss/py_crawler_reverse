import os
import requests
from lxml import etree
from openpyxl import load_workbook
import pandas as pd
import threading
import time
# pyinstaller --onefile longteng.py


class FileUtils:
    @staticmethod
    def mkdirs(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

def geturl(url):
    try:
        res = session.get(url)
        return res
    except Exception as e:
        print('请求报错：',e)
        return None



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                  'Safari/537.36',
}
# headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng," \
#                     "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7 "
# headers['Accept-Encoding'] = "gzip, deflate"
# headers['Accept-Language'] = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"

session = requests.session()
session.headers = headers



cturl_names = []
#获取所有城市URL
res = geturl(f"https://www.lianjia.com/city/")
cturls_html = res.text
tree = etree.HTML(cturls_html)
cturls_htmls = tree.xpath("//div[@class='city_province']//a[starts-with(@href, 'https')]")
for i in range(0, len(cturls_htmls)):
    obj={}
    obj['url']=cturls_htmls[i].attrib['href']+"xiaoqu/" #城市小区URL
    obj['name']=cturls_htmls[i].text
    cturl_names.append(obj)

print(cturl_names)

# 定义一个函数，模拟耗时操作
def task(cturlname):
    output_dir = "./books/"
    FileUtils.mkdirs(folder_path=output_dir)
    output_file_path = os.path.join(output_dir, f"{cturlname['name']}.xlsx")

    # 检查文件是否存在，若不存在则创建
    if not os.path.isfile(output_file_path):
        # 使用pandas创建一个空的Excel文件
        df_empty = pd.DataFrame()
        df_empty.to_excel(output_file_path, sheet_name='MySheet')

    res = geturl(f"{cturlname['url']}")
    if res is None:
        return
    tree = etree.HTML(res.text)
    ct_xqurl_pagenum_text = str(tree.xpath("//div[starts-with(@class, 'page-box')]/@page-data")[0])
    pagenum = int(ct_xqurl_pagenum_text.split(":")[1].split(",")[0])
    cturlname['xqurl_names'] = []  # 当前城市所有小区
    for i in range(1, pagenum + 1):  # 遍历当前城市的所有小区页码
        thread = threading.Thread(target=sub_task, args=(cturlname, i))
        thread.start()

# 定义一个子任务函数
def sub_task(cturlname, i):
    res = geturl(f"{cturlname['url']}pg{i}/")
    if res is None:
        return
    ct_xq_html = res.text
    tree = etree.HTML(ct_xq_html)
    xqurl_name_html = tree.xpath("//div[@class='title']//a[contains(@href, 'xiaoqu')]")
    for j in range(0, len(xqurl_name_html)):  # 遍历当前页面的所有小区
        obj = {}  # 小区对象
        obj['xqname'] = xqurl_name_html[j].text  # 小区名字
        obj['xqurl'] = xqurl_name_html[j].attrib['href']  # 小区URL
        cturlname['xqurl_names'].append(obj)
        res = geturl(obj['xqurl'])
        if res is None:
            continue
        tree = etree.HTML(res.text)
        inf_divs = tree.xpath("//div[contains(@class,'xiaoquInfoItem')]")
        for inf_div in inf_divs:
            # 获取包含 xiaoquInfoLabel 的 span 元素的文本
            label_span = inf_div.xpath(".//span[contains(@class, 'xiaoquInfoLabel')]/text()")
            label_text = label_span[0].strip() if label_span else ""
            # 获取包含 xiaoquInfoContent 的 span 元素的文本
            content_span = inf_div.xpath(".//span[contains(@class, 'xiaoquInfoContent')]/text()")
            content_text = content_span[0].strip() if content_span else ""
            obj[label_text] = content_text
        print(obj)
    time.sleep(1)  # 模拟耗时1秒的操作

# 创建多个线程并启动
threads = []
for cturlname in cturl_names: #遍历所有城市
    thread = threading.Thread(target=task, args=(cturlname))
    threads.append(thread)
    thread.start()

    # 等待所有线程执行完毕
for thread in threads:
    thread.join()