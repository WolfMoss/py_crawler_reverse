import asyncio
import websockets
import json
import uuid

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        print("Connected to WebSocket server")

    async def send_message(self, message):
        if self.websocket is not None:
            await self.websocket.send(message)
            print(f"Message sent to the server: {message}")

    async def receive_messages(self):
        print("开始监听消息")
        while True:
            response = await self.websocket.recv()
            print(f"Message received from the server: {response}")

    async def start(self):
        await self.connect()
        asyncio.create_task(self.receive_messages())

async def main():
    client = WebSocketClient("ws://localhost:8000")

    # 启动WebSocket客户端
    await client.start()


    msg = {
        "action": "send_message",
        "params": {
            "detail_type": "private",
            "user_id": "wxid_ubx9d7ibxeqm22",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "你好"
                    }
                }
            ]
        },
        "echo": str(uuid.uuid4())

    }



    while True:
        # 在代码的其他逻辑中随时调用发送消息
        await client.send_message(json.dumps(msg))

        await asyncio.sleep(5)  # 使用 sleep 来让事件循环继续运行
# 运行客户端
asyncio.run(main())
