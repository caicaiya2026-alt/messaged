import asyncio
import websockets
import json

async def test_client():
    uri = "ws://localhost:8765"
    
    print("正在连接到服务器...")
    try:
        async with websockets.connect(uri) as websocket:
            print("已连接到服务器！")
            print("输入消息并按回车发送 (输入 'quit' 退出):\n")
            
            while True:
                message = input("> ")
                if message.lower() == 'quit':
                    break
                
                data = {
                    "type": "text",
                    "content": message,
                    "timestamp": ""
                }
                
                await websocket.send(json.dumps(data))
                print(f"[已发送] {message}\n")
                
    except ConnectionRefusedError:
        print("连接失败: 服务器未启动或端口错误")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_client())
