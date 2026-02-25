import pyautogui
import time
import sys
import os
from pynput.keyboard import Controller, Listener
from pynput import keyboard

keyboard_controller = Controller()

pyautogui.FAILSAFE = False

# === 全局退出控制变量 ===
should_exit = False

def shoot_when_power_reaches(target_image, timeout=5):
    """ 按住空格，直到目标力度条图片出现后松开 """
    print("开始蓄力...")
    pyautogui.keyDown('space')  # 按住空格
    start_time = time.time()

    while True:
        try:
            power_location = pyautogui.locateOnScreen(target_image, confidence=0.95)
            if power_location:
                print(f"{target_image} 出现，松开空格！")
                pyautogui.keyUp('space')  # 松开空格
                return True
        except pyautogui.ImageNotFoundException:
            pass  # 忽略异常，继续循环

def on_press(key):
    global should_exit
    if key == keyboard.Key.esc:
        print("\n🛑 检测到 Esc，程序即将退出...")
        should_exit = True

listener = Listener(on_press=on_press)
listener.daemon = True
listener.start()

def check_exit():
    if should_exit:
        print("✅ 程序已退出。")
        sys.exit(0)

# ========== 程序开始 ==========
print("欢迎使用圆宇懒惰虫助手！可以随时按下 Esc 键退出程序。")
use_candy = input("是否使用甜食？y/n ").strip().lower() == 'y'

print("程序将在 5 秒后开始运行，请切换到目标窗口...")
time.sleep(5)
print("程序开始运行!")

check_exit()

# 获取资源文件的路径
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# 图片资源路径
img_whistle = os.path.join(base_path, 'whistle_chia.png')
img_ball = os.path.join(base_path, 'ball_chia.png')
img_turn = os.path.join(base_path, 'turn_chia.png')
img_beetle = os.path.join(base_path, 'beetle_chia.png')
img_candy = os.path.join(base_path, 'candy_chia.png')
img_war = os.path.join(base_path, 'war_chia.png')
img_power60 = os.path.join(base_path, 'power_bar_60_chia.png')

bug_images = [
    os.path.join(base_path, 'bug1_chia.png'),
    os.path.join(base_path, 'bug2_chia.png'),
    os.path.join(base_path, 'bug3_chia.png'),
    os.path.join(base_path, 'bug4_chia.png'),
    os.path.join(base_path, 'bug5_chia.png'),
    os.path.join(base_path, 'bug6_chia.png'),
]

def wait_for_image(image_path, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        check_exit()
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location:
                return location
        except:
            pass
        time.sleep(0.5)
    return None

while True:  # 主循环
    check_exit()
    print("\n🔁 开始新一轮")
    candy_used = False
    print("等待哨子出现...")
    if not wait_for_image(img_whistle, timeout=60):
        print("⚠️ 未检测到哨子，重试...")
        continue

    # 如果需要甜食，而且还没点过，就尝试点击甜食
    if use_candy and not candy_used:
        print("🔍 检查是否有甜食...")
        try:
            candy_location = pyautogui.locateOnScreen(img_candy, confidence=0.8)
            if candy_location:
                pyautogui.click(pyautogui.center(candy_location))
                print("🍬 点击了甜食")
                candy_used = True
                time.sleep(0.5)
            else:
                print("⚠️ 没有找到甜食图标")
        except:
            pass

    print("✅ 检测到哨子，开始找虫...")
    clicked_bug = False

    while not clicked_bug:  # 一直找，直到进战斗
        check_exit()

        # 先全程监控 war（防止延迟进入战斗）
        try:
            war_location = pyautogui.locateOnScreen(img_war, confidence=0.85)
            if war_location:
                print("⚔️ 检测到 war（延迟出现），进入战斗")
                clicked_bug = True
                break
        except:
            pass

        for bug_img in bug_images:
            check_exit()
            try:
                bug_location = pyautogui.locateOnScreen(bug_img, confidence=0.8)
                if bug_location:
                    center = pyautogui.center(bug_location)
                    pyautogui.click(center)
                    print(f"点击了 {os.path.basename(bug_img)}，检测是否进入战斗...")

                    # 等 2 秒检测 war
                    start_time = time.time()
                    while time.time() - start_time < 6:
                        check_exit()
                        try:
                            if pyautogui.locateOnScreen(img_war, confidence=0.85):
                                print("⚔️ 检测到 war，进入战斗")
                                clicked_bug = True
                                break
                        except:
                            pass
                        time.sleep(0.1)

                    if clicked_bug:
                        break  # 退出 bug 循环
                    else:
                        print("❌ 6 秒内没检测到 war，继续找虫...")
            except Exception as e:
                print(f"检测虫子时出现异常: {e}")
                continue

        if not clicked_bug:
            try:
                war_location = pyautogui.locateOnScreen(img_war, confidence=0.85)
                if war_location:
                    print("⚔️ 检测到 war（延迟出现），进入战斗")
                    clicked_bug = True
                    break
            except:
                pass

            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width / 2, screen_height / 2)
            print("🎯 点击了屏幕中央")
            try:
                whistle_location = pyautogui.locateOnScreen(img_whistle, confidence=0.8)
                if whistle_location:
                    pyautogui.click(pyautogui.center(whistle_location))
                    print("👉 点击了哨子")
            except:
                pass

    print("开始寻找独角仙及监听 '轮到你了' 状态...")

    turn_count = 0
    beetle_found = False
    start_time = time.time()

    # 检测是否有独角仙
    while True:
        check_exit()
        if time.time() - start_time > 20:
                print("⏱ 超过 20 秒没有轮到我，返回找虫")
                break  # 跳出循环，回到主循环重新找虫
        # 先查独角仙
        try:
            if pyautogui.locateOnScreen(img_beetle, confidence=0.8):
                print("✅ 检测到独角仙，进入独角仙流程")
                beetle_found = True
                break
        except:
            pass

        # 查turn计数
        try:
            if pyautogui.locateOnScreen(img_turn, confidence=0.9):
                print(f"❗️ 检测到第 {turn_count + 1} 次 '轮到你了'")
                turn_count += 1
                start_time = time.time()
                if not beetle_found:
                    if turn_count == 1:
                        pyautogui.press('up', presses=38)  # 修改为45次
                        pyautogui.press('x')
                        pyautogui.keyDown('space')
                        time.sleep(4)
                        pyautogui.keyUp('space')
                    elif turn_count == 2:
                        pyautogui.press('x')
                        pyautogui.keyDown('space')
                        time.sleep(4)
                        pyautogui.keyUp('space')
                    elif turn_count == 3:
                        print("❗️ 第三次turn，无独角仙，执行一次按键动作")
                        pyautogui.press('x')
                        pyautogui.keyDown('space')
                        time.sleep(4)
                        pyautogui.keyUp('space')

                        print("第三次turn动作完成，直接跳出战斗循环，开始新一轮")
                        break  # 跳出战斗检测循环，回到主循环开始新一轮

                # 等待turn消失，避免多次计数
                while True:
                    check_exit()
                    try:
                        if not pyautogui.locateOnScreen(img_turn, confidence=0.9):
                            break
                    except:
                        break
                    time.sleep(0.2)
        except:
            pass

    # 如果检测到独角仙，执行正常独角仙攻击流程
    if beetle_found:
        print("✅ 进入独角仙攻击流程")
        pyautogui.press('up', presses=17)

        turn_count = 0
        print("等待出现三次 '轮到你了'...")
        while turn_count < 3:
            check_exit()
            try:
                if pyautogui.locateOnScreen(img_turn, confidence=0.9):
                    turn_count += 1
                    start_time = time.time()
                    print(f"第 {turn_count} 次检测到 '轮到你了'")
                    if turn_count == 1:
                        print("🔹 第一次攻击：按 1 2 后蓄力")
                        pyautogui.press(['1', '2'])
                        time.sleep(0.2)
                        shoot_when_power_reaches(img_power60)
                    elif turn_count == 2:
                        print("🔹 第二次攻击：按 Z 后蓄力")
                        pyautogui.press('z')
                        time.sleep(0.5)
                        shoot_when_power_reaches(img_power60)
                    elif turn_count == 3:
                        pyautogui.press('up', presses=21)
                        print("🔹 第三次攻击：按 X 后蓄力")
                        pyautogui.press('x')
                        pyautogui.keyDown('space')
                        time.sleep(4)
                        pyautogui.keyUp('space')

                    # 等待 "轮到你了" 消失
                    while True:
                        check_exit()
                        try:
                            if not pyautogui.locateOnScreen(img_turn, confidence=0.9):
                                break
                        except:
                            break
                        time.sleep(0.5)
            except:
                pass
            time.sleep(0.2)

        # 独角仙战斗完成后，等待哨子出现开始新一轮
        print("🔄 独角仙战斗完成，等待哨子出现...")
        # 这里会自动回到主循环的开头