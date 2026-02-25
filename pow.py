import pyautogui
import time
import sys
import os
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
    base_path = sys._MEIPASS  # .exe 临时解压的路径
else:
    base_path = os.path.dirname(__file__)  # IDE 下运行

template_power = [
    os.path.join(base_path, 'power.png'),
]
template_gray_power = [
    os.path.join(base_path, 'gray_power.png'),
]

while count < max_count:
    try:
        time.sleep(0.5)
        power_location = None

        for filename in template_power:
            try:
                print(f"尝试识别: {filename}")
                power_location = pyautogui.locateOnScreen(filename, confidence=0.6)
                if power_location:
                    print(f"成功匹配: {filename} - 位置: {power_location}")
                    break
            except Exception as e:
                print(f"识别图像 {filename} 时发生异常: {e}")

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
                for filename in template_gray_power:
                    try:
                        print(f"尝试识别 gray_power: {filename}")
                        gray_power_location = pyautogui.locateOnScreen(filename, confidence=0.6)
                        if gray_power_location:
                            print(f"成功匹配: {filename} - 位置: {gray_power_location}")
                            break
                    except Exception as e:
                        print(f"识别 gray_power 图像 {filename} 时发生异常: {e}")


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
