import requests
from datetime import datetime
from zoneinfo import ZoneInfo
def get_time_beijing(url):
    response = requests.get(url,verify=False)
    if response.status_code == 200:
        date_time = response.headers['Date']
        date_time_obj = datetime.strptime(date_time, '%a, %d %b %Y %H:%M:%S GMT')
        gmt_time = date_time_obj.replace(tzinfo=ZoneInfo("UTC"))
        beijing_time = gmt_time.astimezone(ZoneInfo("Asia/Shanghai"))
        return beijing_time
    else:
        return None

print(get_time_beijing('https://zwfwdt.tobacco.gov.cn/cooperativeWeb/event/header'))