import json
import time
import os
import wmi
c = wmi.WMI()
import socket
import threading
#验证+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# maxi = 0
# current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# if current_time > "2024-06-08 15:00"  and maxi == 1:
#     print("退出")
#     # 结束整个程序
#     os._exit(0)

hard_disk_serial_number = c.Win32_Processor()[0] #获取CPU序列号

device_from_json={
    "mac_address": hard_disk_serial_number.qualifiers['UUID'],
    "function_name": "validate_customer",
    "data_string": "yuanbaokc_jiankong"
}
yanzhengstr = json.dumps(device_from_json)

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def receive_all(self):
        BUFFER_SIZE = 1024
        data = b''

        while True:
            try:
                part = self.client_socket.recv(BUFFER_SIZE)
                data += part
                if len(part) < BUFFER_SIZE:
                    break
            except:
                return False


        return data.decode('utf-8')

    def send_message(self, msg):
        self.client_socket.send(msg.encode('utf-8'))
        if msg == 'exit':
            self.client_socket.close()
            return

    def start_receiving(self):
        while True:
            data = self.receive_all()
            if not data:
                break
            self.handle_response(data)

    def handle_response(self,response):
        # 在这里处理服务器返回的消息
        print(response)
        if response == 'exit':
            print("退出")
            # 关闭整个程序
            os._exit(0)
        self.client_socket.close()


def method_name():
    client = Client('axiba.idnmd.top', 9999)
    receiving_thread = threading.Thread(target=client.start_receiving)
    receiving_thread.daemon = True
    receiving_thread.start()
    client.send_message(yanzhengstr)

#验证---------------------------------------------------------------------