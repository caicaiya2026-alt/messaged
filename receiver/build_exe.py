import PyInstaller.__main__
import os
import shutil

def build_exe():
    """打包Python接收端为独立的exe文件"""
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller参数
    args = [
        'main.py',                          # 主程序文件
        '--name=消息接收端',                 # 生成的exe名称
        '--onefile',                        # 打包成单个exe文件
        '--windowed',                       # 使用窗口模式（不显示控制台）
        '--clean',                          # 清理临时文件
        '--noconfirm',                      # 覆盖已存在的输出
        '--hidden-import=PyQt6',            # 确保PyQt6被包含
        '--hidden-import=websockets',         # 确保websockets被包含
        '--hidden-import=asyncio',           # 确保asyncio被包含
        '--collect-all',                     # 收集所有依赖
        '--copy-metadata',                  # 复制元数据
        f'--distpath={os.path.join(current_dir, "dist")}',  # 输出目录
        f'--workpath={os.path.join(current_dir, "build")}', # 工作目录
    ]
    
    print("=" * 50)
    print("开始打包消息接收端...")
    print("=" * 50)
    print()
    
    try:
        PyInstaller.__main__.run(args)
        print()
        print("=" * 50)
        print("打包成功！")
        print("=" * 50)
        print()
        
        exe_path = os.path.join(current_dir, 'dist', '消息接收端.exe')
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path)
            print(f"exe文件位置: {exe_path}")
            print(f"文件大小: {file_size / (1024*1024):.2f} MB")
            print()
            print("使用说明:")
            print("1. 将 消息接收端.exe 复制到任何电脑")
            print("2. 双击运行，无需安装 Python")
            print("3. 配置服务器地址和端口")
            print("4. 点击'启动服务器'")
            print()
        else:
            print("警告: 未找到生成的 exe 文件")
            
    except Exception as e:
        print()
        print("=" * 50)
        print("打包失败！")
        print("=" * 50)
        print(f"错误: {e}")
        print()
        print("请检查:")
        print("1. 是否已安装 PyInstaller: pip install pyinstaller")
        print("2. 是否已安装所有依赖: pip install -r requirements.txt")
        print()

if __name__ == "__main__":
    build_exe()
