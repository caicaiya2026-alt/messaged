# 信息发送程序

一个基于 WebSocket 的实时消息传输系统，包含 Python 接收端（桌面应用）和网页发送端。

## 项目结构

```
messaged/
├── receiver/          # Python 接收端
│   ├── main.py        # 主程序（PyQt6 GUI）
│   ├── requirements.txt
│   └── build_exe.py   # 打包脚本
├── sender/            # 网页发送端
│   ├── index.html     # 主页面
│   ├── wrangler.toml  # Cloudflare 配置
│   └── _worker.js     # Cloudflare Functions
└── README.md
```

## 接收端 (Python)

### 功能特性
- PyQt6 图形界面
- WebSocket 服务器
- 实时消息显示
- 支持多客户端连接
- 可配置主机和端口

### 安装依赖

```bash
cd receiver
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

### 打包为 EXE

```bash
python build_exe.py
```

打包后的文件位于 `receiver/dist/消息接收端.exe`

## 发送端 (网页)

### 功能特性
- 响应式设计
- WebSocket 客户端
- 连接状态显示
- 消息发送历史
- 支持 Ctrl+Enter 快速发送

### 本地测试

直接在浏览器中打开 `sender/index.html` 即可测试。

### 部署到 Cloudflare Pages

1. 安装 Wrangler CLI:
```bash
npm install -g wrangler
```

2. 登录 Cloudflare:
```bash
wrangler login
```

3. 部署:
```bash
cd sender
wrangler pages deploy .
```

## 使用说明

### 1. 启动接收端

1. 运行 `消息接收端.exe` 或 `python main.py`
2. 设置主机地址（默认 `0.0.0.0` 监听所有接口）
3. 设置端口（默认 `8765`）
4. 点击"启动服务器"

### 2. 使用发送端

1. 打开网页（本地或 Cloudflare Pages 部署的地址）
2. 输入接收端的 IP 地址和端口
3. 点击"连接服务器"
4. 输入消息内容，点击"发送消息"

### 网络配置

- **本地测试**: 使用 `localhost` 或 `127.0.0.1`
- **局域网**: 使用接收端电脑的局域网 IP（如 `192.168.1.xxx`）
- **公网访问**: 
  - 接收端需要有公网 IP 或使用内网穿透工具（如 frp、ngrok）
  - 配置路由器端口转发

## 技术栈

- **接收端**: Python + websockets + PyQt6
- **发送端**: HTML5 + JavaScript (原生 WebSocket API)
- **部署**: Cloudflare Pages

## 注意事项

1. **防火墙**: 确保接收端电脑的防火墙允许 WebSocket 端口通信
2. **HTTPS**: Cloudflare Pages 使用 HTTPS，如果接收端使用 IP 地址连接，可能需要配置 SSL/TLS
3. **跨域**: 接收端 WebSocket 服务器允许所有来源连接

## 开发计划

- [ ] 消息加密传输
- [ ] 文件传输支持
- [ ] 消息确认机制
- [ ] 用户认证
- [ ] 消息持久化存储
