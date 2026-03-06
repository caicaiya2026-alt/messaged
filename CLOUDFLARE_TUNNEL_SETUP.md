# Cloudflare Tunnel 配置指南

## 已完成
✅ cloudflared 已下载到: `f:\projects\messaged\cloudflared.exe`

## 步骤 1：登录 Cloudflare

在内网电脑B上运行：

```bash
.\cloudflared.exe tunnel login
```

这会打开浏览器，登录你的 Cloudflare 账户并授权。

## 步骤 2：创建 Tunnel

```bash
.\cloudflared.exe tunnel create messaged-tunnel
```

会输出类似：
```
Tunnel ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**请记录这个 Tunnel ID**

## 步骤 3：配置域名路由

将 Tunnel 连接到你的域名：

```bash
.\cloudflared.exe tunnel route dns messaged-tunnel messaged.your-domain.com
```

**将 `your-domain.com` 替换为你的实际域名**

例如：
- 如果域名是 `example.com`，使用 `messaged.example.com`
- 如果域名是 `mydomain.cn`，使用 `messaged.mydomain.cn`

## 步骤 4：创建配置文件

创建 `config.yml` 文件：

```yaml
tunnel: <你的TunnelID>
credentials-file: <你的凭据文件路径>

ingress:
  - hostname: messaged.your-domain.com
    service: tcp://localhost:8765
  - service: http_status:404
```

## 步骤 5：运行 Tunnel

```bash
.\cloudflared.exe tunnel --config config.yml run
```

## 完整示例

假设你的域名是 `example.com`，Tunnel ID 是 `abc123`：

```bash
# 1. 登录
.\cloudflared.exe tunnel login

# 2. 创建 Tunnel
.\cloudflared.exe tunnel create messaged-tunnel
# 输出: Tunnel ID: abc123-def456-ghi789

# 3. 配置域名
.\cloudflared.exe tunnel route dns messaged-tunnel messaged.example.com

# 4. 运行 Tunnel
.\cloudflared.exe tunnel run messaged-tunnel
```

## 发送端配置

在外网电脑A的 Cloudflare Pages 页面中：

- **服务器地址**: `messaged.example.com`
- **端口**: `443`（自动使用 wss://）

## 测试步骤

### 内网电脑B

1. 启动接收端：
```bash
cd receiver
python main.py
```

2. 启动 Tunnel：
```bash
.\cloudflared.exe tunnel run messaged-tunnel
```

### 外网电脑A

1. 打开发送端：https://55bfc4c2.messaged-sender.pages.dev
2. 输入服务器地址：`messaged.example.com`
3. 端口：`443`
4. 点击"连接服务器"
5. 发送消息测试

## 注意事项

1. **域名必须添加到 Cloudflare**：确保你的域名已添加到 Cloudflare DNS
2. **防火墙**：确保内网电脑B的防火墙允许连接
3. **DNS 传播**：域名配置可能需要几分钟生效
4. **Tunnel 持续运行**：Tunnel 需要保持运行状态

## 自动启动脚本

创建 `start-tunnel.bat`：

```batch
@echo off
echo Starting Message Receiver...
start cmd /k "cd receiver && python main.py"
timeout /t 3
echo Starting Cloudflare Tunnel...
.\cloudflared.exe tunnel run messaged-tunnel
```

双击此脚本即可自动启动接收端和 Tunnel。
