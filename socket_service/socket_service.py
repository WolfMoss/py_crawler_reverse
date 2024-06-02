import json
import socket
import threading
import traceback

#定义方法++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def to_json(obj):
    return json.dumps(obj.to_dict())

def from_json(json_str):
    data = json.loads(json_str)
    return NetworkDevice.from_dict(data)

class NetworkDevice:
    def __init__(self, ip_address, mac_address, function_name, data_string):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.function_name = function_name
        self.data_string = data_string

    def to_dict(self):
        return {
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "function_name": self.function_name,
            "data_string": self.data_string
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["ip_address"],
            data["mac_address"],
            data["function_name"],
            data["data_string"]
        )
# 创建类实例++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
device = NetworkDevice("192.168.1.100", "00:1A:2B:3C:4D:5E", "router", "Data String 1")
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
    device_from_json.ip_address =addr
    # 根据函数名调用不同方法
    if function_name in FUNCTION_MAP:
        function = FUNCTION_MAP[function_name]
        return function(device_from_json)
    else:
        print(f"Function {function_name} does not exist in FUNCTION_MAP.")

#服务启动------------------------------------------------------------------------

#业务方法+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def function_a(device):
    print(f"Executing Function A for device with IP {device.ip_address}")
    return "Function A executed successfully"

def function_b(device):
    print(f"Executing Function B for device with IP {device.ip_address}")
    return "Function B executed successfully"

def function_c(device):
    print(f"Executing Function C for device with IP {device.ip_address}")
    return "Function C executed successfully"

FUNCTION_MAP = {
    "function_a": function_a,
    "function_b": function_b,
    "function_c": function_c
}
#业务方法-------------------------------------------------------------------------

if __name__ == '__main__':
    start_server()