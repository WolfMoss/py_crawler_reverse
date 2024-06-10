import json
import socket
import threading
import time
import traceback
import pymysql

#定义方法++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def to_json(obj):
    return json.dumps(obj.to_dict())

def from_json(json_str):
    data = json.loads(json_str)
    return NetworkDevice.from_dict(data)

class NetworkDevice:
    def __init__(self, mac_address, function_name, data_string):
        self.mac_address = mac_address
        self.function_name = function_name
        self.data_string = data_string

    def to_dict(self):
        return {
            "mac_address": self.mac_address,
            "function_name": self.function_name,
            "data_string": self.data_string
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["mac_address"],
            data["function_name"],
            data["data_string"]
        )
# 创建类实例++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
device = NetworkDevice("00:1A:2B:3C:4D:5E", "router", "Data String 1")
# 类实例转换为 JSON 字符串
json_str = to_json(device)
# JSON 字符串转换回类实例
device_from_json = from_json(json_str)
#创建类实例-----------------------------------------------------------------------
#定义方法------------------------------------------------------------------------------------

#服务启动++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def handle_client(client_socket, addr):
    def receive_all(sock):
        BUFFER_SIZE = 1024  # 每次接收的数据块大小
        data = b''  # 用于存储接收的所有数据

        while True:
            part = sock.recv(BUFFER_SIZE)
            data += part
            if len(part) < BUFFER_SIZE:  # 如果接收到的数据块小于 BUFFER_SIZE，说明数据接收完毕
                break

        return data.decode('utf-8')

    while True:
        # 接收来自客户端的数据
        data = receive_all(client_socket)
        print(f"从 {addr} 接收到消息: {data}")
        if not data:
            break
        try:
            resdata = get_msg_seng(data,addr)
            # 发送消息给客户端
            client_socket.send(resdata.encode('utf-8'))
        except Exception as e:
            traceback.print_exc()
    client_socket.close()

def start_server():
    # 创建 socket 对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取本地主机名
    host = '0.0.0.0'
    port = 9999

    # 绑定端口
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("服务器启动，等待客户端连接...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"客户端 {addr} 已连接")

        # 为每个客户端创建一个新的线程来处理连接
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

#接受消息并返回
def get_msg_seng(data,addr):
    device_from_json = from_json(data)
    function_name=device_from_json.function_name
    # 根据函数名调用不同方法
    if function_name in FUNCTION_MAP:
        function = FUNCTION_MAP[function_name]
        return function(device_from_json)
    else:
        print(f"Function {function_name} does not exist in FUNCTION_MAP.")

#服务启动------------------------------------------------------------------------

#业务方法+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def validate_customer(device):
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        data_string=device.data_string



        # 遍历 Customers 列表
        incustomer = False
        for customer in config["Customers"]:
            if data_string in customer["name"]:
                incustomer=True
                outdate = customer["date"]
                usenum = customer['usenum']
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if current_time > outdate:
                    print("过期")
                    return "exit"
                else:
                    print("未过期")

                    db = pymysql.connect(host='axiba.idnmd.top', user='root', passwd='ilikecs123!', port=8306,
                                         db='quant')

                    cursor = db.cursor()
                    cursor.execute(f"SELECT * FROM jiedan_key WHERE hard_disk_serial_number='{device.mac_address}' and func_name='{customer['name']}'")
                    results = cursor.fetchall()
                    if len(results) > 0:
                        db.close()
                        return "1"

                    cursor.execute(
                        f"SELECT * FROM jiedan_key WHERE func_name='{customer['name']}'")
                    results = cursor.fetchall()
                    if len(results)+1 > usenum:
                        print("超出使用量限制")
                        db.close()
                        return "exit"

                    cursor.execute(
                        f"INSERT INTO jiedan_key (func_name, hard_disk_serial_number,is_used) VALUES ('{customer['name']}', '{device.mac_address}', 1)")

                    # 提交事务
                    db.commit()
                    db.close()

                    return "1"


        if not incustomer :
            print("客户不在列表")
            return "exit"


def function_b(device):
    print(f"Executing Function B for device with IP {device.mac_address}")
    return "Function B executed successfully"

def function_c(device):
    print(f"Executing Function C for device with IP {device.mac_address}")
    return "Function C executed successfully"

FUNCTION_MAP = {
    "validate_customer": validate_customer,
    "function_b": function_b,
    "function_c": function_c
}
#业务方法-------------------------------------------------------------------------

if __name__ == '__main__':
    start_server()