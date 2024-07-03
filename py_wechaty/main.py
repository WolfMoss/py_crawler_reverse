import asyncio
import websockets

async def connect_to_websocket():
    uri = "ws://localhost:7600/wcf/socket_receiver"
    async with websockets.connect(uri) as websocket:
        # 持续发送和接收消息
        while True:
            # 接收消息
            response = await websocket.recv()
            print(f"Message received from the server: {response}")

# 运行客户端
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
