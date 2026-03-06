import PyInstaller.__main__
import os

def build_exe():
    """打包Python接收端为exe文件"""
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller参数
    args = [
        'main.py',                          # 主程序文件
        '--name=消息接收端',                 # 生成的exe名称
        '--onefile',                        # 打包成单个exe文件
        '--windowed',                       # 使用窗口模式（不显示控制台）
        '--icon=NONE',                      # 可以添加图标文件路径
        '--clean',                          # 清理临时文件
        '--noconfirm',                      # 覆盖已存在的输出
        f'--distpath={os.path.join(current_dir, "dist")}',  # 输出目录
        f'--workpath={os.path.join(current_dir, "build")}', # 工作目录
        '--add-data=requirements.txt;.',    # 包含requirements.txt
    ]
    
    print("开始打包...")
    PyInstaller.__main__.run(args)
    print("打包完成！")
    print(f"exe文件位于: {os.path.join(current_dir, 'dist', '消息接收端.exe')}")

if __name__ == "__main__":
    build_exe()
