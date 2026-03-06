import asyncio
import websockets
import json
from datetime import datetime

clients = set()

async def register(websocket):
    clients.add(websocket)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 客户端已连接 (当前: {len(clients)}个)")

async def unregister(websocket):
    clients.discard(websocket)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 客户端已断开 (当前: {len(clients)}个)")

async def handle_client(websocket):
    await register(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                content = data.get('content', '')
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[{timestamp}] 收到消息: {content}")
                print(f"来自: {websocket.remote_address}")
                print("-" * 50)
            except json.JSONDecodeError:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 收到原始消息: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister(websocket)

async def main():
    host = "0.0.0.0"
    port = 8765
    
    print("=" * 50)
    print("WebSocket 消息接收服务器")
    print("=" * 50)
    print(f"服务器地址: ws://{host}:{port}")
    print(f"本地访问: ws://localhost:{port}")
    print(f"局域网访问: ws://<本机IP>:{port}")
    print("=" * 50)
    print("等待连接... (按 Ctrl+C 停止)\n")
    
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # 永久运行

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
