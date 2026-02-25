import pyautogui
import time

# 等待 2 秒，确保程序启动后有时间切换窗口
time.sleep(5)

while True:
    # 识别 'mine.png'
    location = pyautogui.locateCenterOnScreen('mine.png', confidence=0.8,grayscale=True)
    # 识别 'flag.png'
    flag_location = pyautogui.locateCenterOnScreen('flag.png', confidence=0.8)

    if location and flag_location:
        # 点击 flag 位置
        pyautogui.moveTo(flag_location.x,flag_location.y)
        pyautogui.click(flag_location.x, flag_location.y)
        time.sleep(0.2)  # 等待点击完成

        # 移动到 mine 位置
        pyautogui.moveTo(location.x, location.y, duration=0.2)
        pyautogui.click()
        time.sleep(0.2)  # 等待点击完成
    else:
        print("No more 'mine.png' detected, exiting loop.")
        break  # 退出循环
