import socket
import threading

def handle_client(client_socket, addr):
    while True:
        # 接收来自客户端的数据
        data = client_socket.recv(1024).decode('utf-8')
        print(f"从 {addr} 接收到消息: {data}")
        if not data:
            break
        # 发送消息给客户端
        client_socket.send('消息已收到'.encode('utf-8'))
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

if __name__ == '__main__':
    start_server()