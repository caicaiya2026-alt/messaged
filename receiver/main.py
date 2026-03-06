import asyncio
import websockets
import json
import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QLineEdit, QSpinBox, QStatusBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class WebSocketServer(QThread):
    message_received = pyqtSignal(str, str)
    connection_status = pyqtSignal(str)
    
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.running = False
        self.clients = set()
        
    async def register(self, websocket):
        self.clients.add(websocket)
        self.connection_status.emit(f"客户端已连接 (当前: {len(self.clients)}个)")
        
    async def unregister(self, websocket):
        self.clients.discard(websocket)
        self.connection_status.emit(f"客户端已断开 (当前: {len(self.clients)}个)")
        
    async def handle_client(self, websocket):
        await self.register(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get('type', 'text')
                    content = data.get('content', '')
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.message_received.emit(timestamp, content)
                except json.JSONDecodeError:
                    self.message_received.emit(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        f"[原始消息] {message}"
                    )
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def start_server(self):
        self.running = True
        async with websockets.serve(self.handle_client, self.host, self.port):
            self.connection_status.emit(f"服务器已启动: ws://{self.host}:{self.port}")
            while self.running:
                await asyncio.sleep(1)
    
    def run(self):
        asyncio.run(self.start_server())
    
    def stop(self):
        self.running = False


class MessageReceiver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("消息接收端")
        self.setGeometry(100, 100, 600, 500)
        
        self.server = None
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 服务器设置区域
        settings_layout = QHBoxLayout()
        
        settings_layout.addWidget(QLabel("主机:"))
        self.host_input = QLineEdit("0.0.0.0")
        self.host_input.setFixedWidth(120)
        settings_layout.addWidget(self.host_input)
        
        settings_layout.addWidget(QLabel("端口:"))
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(8765)
        self.port_input.setFixedWidth(80)
        settings_layout.addWidget(self.port_input)
        
        settings_layout.addStretch()
        
        self.start_btn = QPushButton("启动服务器")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_btn.clicked.connect(self.toggle_server)
        settings_layout.addWidget(self.start_btn)
        
        layout.addLayout(settings_layout)
        
        # 消息显示区域
        layout.addWidget(QLabel("接收到的消息:"))
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        self.message_display.setFont(QFont("Consolas", 10))
        layout.addWidget(self.message_display)
        
        # 清除按钮
        self.clear_btn = QPushButton("清除消息")
        self.clear_btn.clicked.connect(self.clear_messages)
        layout.addWidget(self.clear_btn)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
    def toggle_server(self):
        if self.server is None:
            host = self.host_input.text()
            port = self.port_input.value()
            
            self.server = WebSocketServer(host, port)
            self.server.message_received.connect(self.on_message_received)
            self.server.connection_status.connect(self.on_connection_status)
            self.server.start()
            
            self.start_btn.setText("停止服务器")
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            self.host_input.setEnabled(False)
            self.port_input.setEnabled(False)
        else:
            self.server.stop()
            self.server = None
            
            self.start_btn.setText("启动服务器")
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.host_input.setEnabled(True)
            self.port_input.setEnabled(True)
            self.status_bar.showMessage("服务器已停止")
    
    def on_message_received(self, timestamp, content):
        self.message_display.append(f"[{timestamp}] {content}")
    
    def on_connection_status(self, status):
        self.status_bar.showMessage(status)
    
    def clear_messages(self):
        self.message_display.clear()
    
    def closeEvent(self, event):
        if self.server:
            self.server.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MessageReceiver()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
