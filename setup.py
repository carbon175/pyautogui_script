"""
自动化脚本环境安装程序
支持 Windows, macOS, Linux
"""

import subprocess
import sys
import platform
import os

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("错误: 需要Python 3.7或更高版本")
        return False
    return True

def install_system_dependencies():
    """安装系统依赖"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("macOS系统检测到")
        print("请确保已安装Xcode命令行工具:")
        print("  xcode-select --install")
        
    elif system == "Linux":
        print("Linux系统检测到")
        print("如果遇到OpenCV安装问题，请先安装系统依赖:")
        print("  Ubuntu/Debian: sudo apt-get install libopencv-dev python3-opencv")
        print("  CentOS/RHEL: sudo yum install opencv-devel")
        
    elif system == "Windows":
        print("Windows系统检测到")
        print("通常不需要额外的系统依赖")

def main():
    print("="*60)
    print("自动化脚本环境安装程序")
    print("="*60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 显示系统信息
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    
    # 安装系统依赖提示
    install_system_dependencies()
    
    # 要安装的包列表
    packages = [
        "pyautogui",
        "opencv-python", 
        "numpy",
        "pynput",
        "pillow"  # 有时pyautogui需要
    ]
    
    print(f"\n开始安装Python包...")
    print("-"*40)
    
    failed_packages = []
    
    for package in packages:
        print(f"正在安装 {package}...")
        if install_package(package):
            print(f"✓ {package} 安装成功")
        else:
            print(f"✗ {package} 安装失败")
            failed_packages.append(package)
    
    print("-"*40)
    
    if failed_packages:
        print(f"以下包安装失败: {failed_packages}")
        print("请手动安装:")
        for package in failed_packages:
            print(f"  pip install {package}")
    else:
        print("所有依赖包安装成功!")
    
    # 创建示例配置文件
    config_content = """{
  "threshold": 0.65,
  "scales": [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
  "retry_count": 10,
  "timeout": 600,
  "click_duration": 0.2,
  "key_delay": 0.1
}"""
    
    config_file = "automation_config.json"
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"✓ 已创建配置文件: {config_file}")
    
    # 权限提醒
    system = platform.system()
    if system == "Darwin":
        print("\n" + "="*60)
        print("macOS 权限设置提醒")
        print("="*60)
        print("请按以下步骤设置权限:")
        print("1. 打开 系统偏好设置")
        print("2. 选择 安全性与隐私")
        print("3. 点击 隐私 标签页")
        print("4. 选择 辅助功能")
        print("5. 点击锁图标解锁")
        print("6. 添加终端或Python到允许列表")
        print("7. 重启终端")
    
    elif system == "Linux":
        print("\n" + "="*60)
        print("Linux 权限提醒")
        print("="*60)
        print("如果遇到权限问题，可能需要:")
        print("1. 将用户添加到input组: sudo usermod -a -G input $USER")
        print("2. 安装X11开发包 (如果使用X11)")
        print("3. 重新登录使组权限生效")
    
    print("\n" + "="*60)
    print("安装完成!")
    print("="*60)
    print("请确保以下文件在脚本目录中:")
    print("  - power.png")
    print("  - gray_power.png")
    print("  - automation_config.json (已自动创建)")
    print("\n现在可以运行主脚本了!")

if __name__ == "__main__":
    main()