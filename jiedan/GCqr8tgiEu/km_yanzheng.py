import os
import wmi
import requests
c = wmi.WMI()
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 忽略 HTTPS 安全警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def method_name(fuc_km):

    hard_disk_serial_number = c.Win32_ComputerSystemProduct()[0]  # 获取CPU序列号
    print(hard_disk_serial_number.UUID)
    url = f"https://km.idnmd.top/?key={fuc_km}&cpuid={hard_disk_serial_number.UUID}"
    #get请求
    res = requests.get(url, verify=False)
    print(res.text)
    if res.text != '1':
        print("退出")
        # 关闭整个程序
        os._exit(0)

method_name("111")