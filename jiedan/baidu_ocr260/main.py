import json
import requests
import fitz
from PIL import Image
from urllib.parse import urlencode
import base64
import glob
import yanzheng
import pandas as pd
import io
import sys
print(sys.path)

yanzheng.method_name('baidu_ocr260')
maxi=0

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

API_KEY = "BC2QycCBuRm0F4hef8u3CxId"
SECRET_KEY = "Yf1D0MQztWv04QrkW6oXGP5Kg542oGaY"
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





def main(pdfpath):
    image = convert_pdf_to_images(pdfpath)

    image1 = resize_image(image)
    img_base64 = image_to_base64(image1)
    img_urlencoded = urlencode({'': img_base64})[1:]
    if len(img_urlencoded) <= 4 * 1024 * 1024:  # 4MB
        print(pdfpath,"格式校验通过")
    else:
        print("Encoded image is larger than 4MB.")

    url = "https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise?access_token=" + access_token

    payload = f'image={img_urlencoded}&templateSign=0f3a3129abf349d6f5f9bbf6eeedf231'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def findjsonkey(json_obj, key):
    # 遍历查找word_name为'户名'的word
    for item in json_obj['data']['ret']:
        if item['word_name'] == key:
            return item['word']
            break

# 读取Excel文件
df = pd.read_excel('业务信息模板.xlsx', sheet_name='Sheet1')
# 将DataFrame转换为JSON
json_data = df.to_json(orient='records', force_ascii=False)
json_data=json.loads(json_data)

excel_json =[]

# 获取当前目录及所有子目录下的PDF文件
pdf_files = glob.glob('pdfs/*.pdf', recursive=True)
i=0
# 打印出每个文件的路径
for file in pdf_files:
    if i>=1 and maxi==1:
        break
    print(file)
    pdfjson = main(file)
    excel_line_obj = {}
    excel_line_obj['户名']=findjsonkey(pdfjson, '户名')
    dkje = findjsonkey(pdfjson, '贷款金额').replace(',', '').replace('，', '').replace('.', '')
    excel_line_obj['贷款金额'] = float(dkje[:-2]+ '.' + dkje[-2:])/10000
    excel_line_obj['流水号'] = findjsonkey(pdfjson, '额度项下提款流水号')
    ebj = findjsonkey(pdfjson, '额度项下提款本金').replace(',', '').replace('，', '').replace('.', '')
    excel_line_obj['发生额本金'] = float(ebj[:-2]+ '.' + ebj[-2:])/10000
    excel_line_obj['交易日期'] = findjsonkey(pdfjson, '额度项下提款交易日期')
    excel_line_obj['交易类型']=''

    findmb = False
    for item in json_data:
        if float(item['合同金额（万元）']) ==float(excel_line_obj['贷款金额']) and item['法定代表人姓名'] == excel_line_obj['户名']:
            excel_line_obj['业务编号'] = item['业务编号']
            excel_line_obj['债务人名称'] = item['客户名称']
            excel_line_obj['债务人证件号码'] = item['债务人证件号码']
            findmb = True
            break
    if not findmb:
        excel_line_obj['业务编号'] = ""
        excel_line_obj['债务人名称'] = ""
        excel_line_obj['债务人证件号码'] = ""

    excel_json.append(excel_line_obj)
    i=i+1

print(excel_json)

# 将JSON数据转换为DataFrame
df = pd.DataFrame(excel_json)
# 指定列的顺序，如果有额外的列，也可以在这里添加
columns_order = ['户名', '业务编号', '债务人名称', '债务人证件号码', '贷款金额', '流水号', '交易类型', '发生额本金', '交易日期']
# 重新排列DataFrame的列顺序
df = df[columns_order]
# 写入Excel文件，如果文件不存在，pandas会自动创建
df.to_excel('用款流水登记台账模板.xlsx', index=False, engine='openpyxl')



