import pyautogui
import time
import sys
import os
import json
from pynput.keyboard import Controller, Key


keyboard = Controller()
count = 0
max_count = int(input("请输入目标计数 (例如 2): "))
timeout = 600  
start_time = time.time()
max_retries = 10
pyautogui.FAILSAFE = True

print("程序将在5秒后开始运行，请切换到目标窗口...")
time.sleep(5)  
print("程序开始运行!")

# 获取资源文件的路径
if getattr(sys, 'frozen', False):
    # .exe 运行时，从 exe 所在目录读取配置文件
    base_path = os.path.dirname(sys.executable)
else:
    # Python 脚本运行时
    base_path = os.path.dirname(os.path.abspath(__file__))

# 读取配置文件
config_path = os.path.join(base_path, 'config.json')
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    print(f"成功加载配置文件: {config_path}")
except FileNotFoundError:
    print(f"错误: 配置文件不存在 {config_path}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"错误: 配置文件格式错误 - {e}")
    sys.exit(1)

# 解析配置
template_power = []
template_gray_power = []

for item in config.get('power', []):
    parts = item.split()
    if len(parts) == 2:
        filename, confidence = parts[0], float(parts[1])
        template_power.append({
            'path': os.path.join(base_path, filename),
            'confidence': confidence
        })

for item in config.get('gray_power', []):
    parts = item.split()
    if len(parts) == 2:
        filename, confidence = parts[0], float(parts[1])
        template_gray_power.append({
            'path': os.path.join(base_path, filename),
            'confidence': confidence
        })

print(f"加载 {len(template_power)} 个 power 模板")
print(f"加载 {len(template_gray_power)} 个 gray_power 模板")

while count < max_count:
    try:
        time.sleep(0.5)
        power_location = None

        for template in template_power:
            try:
                print(f"尝试识别: {template['path']} (confidence={template['confidence']})")
                power_location = pyautogui.locateOnScreen(
                    template['path'], 
                    confidence=template['confidence']
                )
                if power_location:
                    print(f"成功匹配: {template['path']} - 位置: {power_location}")
                    break
            except Exception as e:
                print(f"识别图像 {template['path']} 时发生异常: {e}")

        if power_location:
            center_x, center_y = pyautogui.center(power_location)
            pyautogui.moveTo(center_x, center_y, duration=0.2)

            retries = 0
            while retries < max_retries:
                pyautogui.press('b', presses=3)
                pyautogui.mouseDown()
                pyautogui.click()
                time.sleep(0.5)
                pyautogui.mouseUp()

                if count == max_count - 1:
                    print("计数达到目标-1，按住 'right' 键...")
                    for _ in [0.1, 3, 0.1]:
                        pyautogui.keyDown('right')
                        time.sleep(_)
                        pyautogui.keyUp('right')
                    print('程序结束')
                    sys.exit(0)
                else:
                    pyautogui.press('p')
                    time.sleep(0.5)

                gray_power_location = None
                for template in template_gray_power:
                    try:
                        print(f"尝试识别 gray_power: {template['path']} (confidence={template['confidence']})")
                        gray_power_location = pyautogui.locateOnScreen(
                            template['path'], 
                            confidence=template['confidence']
                        )
                        if gray_power_location:
                            print(f"成功匹配: {template['path']} - 位置: {gray_power_location}")
                            break
                    except Exception as e:
                        print(f"识别 gray_power 图像 {template['path']} 时发生异常: {e}")

                if gray_power_location:
                    count += 1
                    print(f"当前计数: {count}/{max_count}")
                    break
                else:
                    print(f"未检测到 gray_power，重试 {retries + 1}/{max_retries}...")
                    retries += 1

            if retries == max_retries:
                print("多次点击后仍未检测到 gray_power，可能点击失败。")

        else:
            pyautogui.press('p')
            print("未找到 power 图像，继续按 P。")

    except Exception as e:
        error_type = type(e).__name__  
        print(f"发生错误: {error_type} - {str(e)}")
        print("继续按 P 键...")
        pyautogui.press('p')

    if time.time() - start_time > timeout:
        print("操作超时!")
        break

print("程序执行完毕")