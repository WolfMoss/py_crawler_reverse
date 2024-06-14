import json
import requests
import fitz
from PIL import Image
from urllib.parse import urlencode
import base64
import glob
import time
import pandas as pd
from io import BytesIO
import os
import pandas as pd
import io

import yanzheng
yanzheng.method_name('baidu_ocr400')
maxi=0

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

API_KEY = "SXZ6Ym9WTySuuNPjKmf1R7gb"
SECRET_KEY = "lKNufVSBDn8hfwZm5poZB5kcdfpbI5OO"
access_token = get_access_token()

def convert_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)

    page = doc.load_page(0)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img

def resize_image(image):
    max_size = 4096
    min_size = 15
    width, height = image.size
    if width > max_size or height > max_size:
        scaling_factor = min(max_size / width, max_size / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        image = image.resize(new_size, Image.ANTIALIAS)
    if image.size[0] < min_size or image.size[1] < min_size:
        raise ValueError("Image size is too small after resizing.")
    return image

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def get_pdf_header(pdfpath):
    image = convert_pdf_to_images(pdfpath)

    image1 = resize_image(image)
    img_base64 = image_to_base64(image1)
    img_urlencoded = urlencode({'': img_base64})[1:]
    if len(img_urlencoded) <= 4 * 1024 * 1024:  # 4MB
        print(pdfpath,"格式校验通过")
    else:
        print("Encoded image is larger than 4MB.")

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + access_token

    payload = f'image={img_urlencoded}&detect_direction=false&paragraph=false&probability=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

def get_pdf_rows(pdfpath):
    # 读取PDF文件并编码为Base64字符串
    with open(pdfpath, 'rb') as pdf_file:
        pdf_data = pdf_file.read()
        base64_pdf_str = base64.b64encode(pdf_data).decode('utf-8')
        img_urlencoded = urlencode({'': base64_pdf_str})[1:]

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/table?access_token=" + access_token

    payload = f'pdf_file={img_urlencoded}&cell_contents=false&return_excel=true'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

def findjsonkey(json_obj, key):
    # 遍历查找word_name为'户名'的word
    for item in json_obj['data']['ret']:
        if item['word_name'] == key:
            return item['word']
            break

# 读取Excel文件
df = pd.read_excel('业务信息模板.xlsx', sheet_name='Sheet1')
# 将DataFrame转换为JSON
json_data_mb = df.to_json(orient='records', force_ascii=False)
json_data_mb=json.loads(json_data_mb)
excel_json =[]

# 获取当前目录及所有子目录下的PDF文件
pdf_files = glob.glob('pdfs400/*.pdf', recursive=True)
i=0
# 打印出每个文件的路径
for file in pdf_files:
    if i>=1 and maxi==1:
        break
    response=get_pdf_header(file)
    responsetext = response.text
    responsejson = response.json()

    hm = responsetext.split('户名：')[1].split('"')[0]

    dkje = responsetext.split('贷款金额：')[1].split('"')[0].replace(',', '').replace('，', '').replace('.', '')
    dkje = float(dkje[:-2]+ '.' + dkje[-2:])/10000

    #  交易日期 交易类型 发生额本金 流水号
    response_rows = get_pdf_rows(file)
    response_rowstext = response_rows.text
    response_rowsjson = response_rows.json()
    excelbase64 = response_rowsjson['excel_file']

    # 解码Base64字符串为二进制数据
    excel_data = base64.b64decode(excelbase64)
    # 使用BytesIO将二进制数据转换为文件对象
    excel_file = BytesIO(excel_data)
    # 读取Excel文件，从第三行开始
    df = pd.read_excel(excel_file, skiprows=1, nrows=40)
    # 重命名列
    df.columns = ['序号', '交易日期', '交易类型', '发生额合计', '发生额本金', '发生额利息', '发生额罚息', '本金余额', '流水号']
    # 将DataFrame转换为JSON
    json_data = df.to_json(orient='records', force_ascii=False)
    json_data = json.loads(json_data)
    dkje=None
    for row in json_data:
        if not row['交易日期']:
            continue
        excel_line_obj = {}

        if row['交易类型']=='信用额度开户':
            print("贷款金额取信用额度开户")
            dkje = row['发生额合计'].replace(',', '').replace('，', '').replace('.', '')
            dkje = float(dkje[:-2] + '.' + dkje[-2:]) / 10000


        fsebj= row['发生额本金'].replace(',', '').replace('，', '').replace('.', '')
        row['发生额本金'] = float(fsebj[:-2] + '.' + fsebj[-2:]) / 10000
        if row['发生额本金']==0:
            continue


        excel_line_obj['户名'] =hm
        excel_line_obj['交易日期'] = row['交易日期']
        excel_line_obj['交易类型'] = row['交易类型']
        excel_line_obj['发生额本金'] = row['发生额本金']
        excel_line_obj['流水号'] = row['流水号']
        excel_line_obj['贷款金额'] = dkje




        findmb = False
        for item in json_data_mb:
            if float(item['合同金额（万元）']) ==float(excel_line_obj['贷款金额']) and item['法定代表人姓名'] == excel_line_obj['户名']:
                excel_line_obj['业务编号'] = item['业务编号']
                excel_line_obj['债务人名称'] = item['客户名称']
                excel_line_obj['债务人证件号码'] = item['债务人证件号码']
                findmb = True
                break

        if not findmb:
            continue
            excel_line_obj['业务编号'] = ""
            excel_line_obj['债务人名称'] = ""
            excel_line_obj['债务人证件号码'] =""

        excel_json.append(excel_line_obj)
    i=i+1


# 将JSON数据转换为DataFrame
df = pd.DataFrame(excel_json)
# 指定列的顺序，如果有额外的列，也可以在这里添加
columns_order = ['户名', '业务编号', '债务人名称', '债务人证件号码', '贷款金额', '流水号', '交易类型', '发生额本金', '交易日期']
# 重新排列DataFrame的列顺序
df = df[columns_order]
# 然后，将需要设置为纯文本格式的列转换为字符串
text_columns = ['户名', '业务编号', '债务人名称', '债务人证件号码', '贷款金额', '流水号', '交易类型', '发生额本金', '交易日期']  # 举例，这些列需要转换为文本
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str)
# 写入Excel文件，如果文件不存在，pandas会自动创建
df.to_excel('用款流水登记台账模板.xlsx', index=False, engine='openpyxl')



