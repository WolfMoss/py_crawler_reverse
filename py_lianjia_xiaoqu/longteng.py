import os
import requests
from lxml import etree
from openpyxl import load_workbook
import pandas as pd
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
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


futures = []
lock = Lock()

# 定义一个函数，用于处理单个的城市
def process_city(cturlname):
    # 该函数中的代码基本上是从原来的城市循环中复制过来的
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
    cturlname['xqurl_names']=[] #当前城市所有小区


    # 定义一个函数，用于处理单个小区
    def process_xq(i):
        # 该函数中的代码基本上是从原来的小区循环中复制过来的
        res = geturl(f"{cturlname['url']}pg{i}/")
        if res is None:
            return
        ct_xq_html = res.text
        tree = etree.HTML(ct_xq_html)
        xqurl_name_html = tree.xpath("//div[@class='title']//a[contains(@href, 'xiaoqu')]")
        for j in range(0, len(xqurl_name_html)): #遍历当前页面的所有小区
            obj={} #小区对象
            obj['xqname']=xqurl_name_html[j].text #小区名字
            obj['xqurl']=xqurl_name_html[j].attrib['href'] #小区URL
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
                obj[label_text]=content_text

            # ... 小区处理操作
            with lock:  # 获取锁
                # 写入文件的代码
                try:
                    # 载入已存在的文件
                    book = load_workbook(output_file_path)
                    # 读取已存在的文件
                    df_old = pd.read_excel(output_file_path, index_col=0)
                    # 读取已存在的数据
                    df_old = pd.read_excel(output_file_path, sheet_name='MySheet', engine='openpyxl')
                    # 这里创建一份新的数据添加到旧数据后面，your_new_data 是你需要添加的内容
                    df_new = pd.DataFrame(obj,index=[0])
                    # 将新数据添加到旧数据后面
                    df = pd.concat([df_old, df_new])
                    df.to_excel(output_file_path, sheet_name='MySheet', index=False, engine='openpyxl')  # For writing



                    print(obj)
                except Exception as e:
                    print(f"写入数据时发生错误：{str(e)}")
                # ...

    # 在城市函数内部创建线程池处理小区任务
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        # 提交小区任务
        for i in range(1, pagenum + 1):
            futures.append(executor.submit(process_xq, i))

        for future in as_completed(futures):
            future.result()  # 这里我们不需要获取任务的返回值

    return cturlname

# 创建 ThreadPoolExecutor 对象，与你的 CPU 核心数相同
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    # 将城市任务提交给线程池
    for cturlname in cturl_names:
        futures.append(executor.submit(process_city, cturlname))

    for future in as_completed(futures):
        result = future.result() # 这里的result就是process_city函数的返回值
        print(result)

executor.shutdown()




