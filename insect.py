import pyautogui
import time
import sys
import os
import json
from datetime import datetime
from pynput.keyboard import Controller, Listener
from pynput import keyboard

keyboard_controller = Controller()
pyautogui.FAILSAFE = False

# === 全局退出控制变量 ===
should_exit = False

def on_press(key):
    global should_exit
    if key == keyboard.Key.esc:
        log_print("\n🛑 检测到 Esc，程序即将退出...")
        should_exit = True

listener = Listener(on_press=on_press)
listener.daemon = True
listener.start()

def check_exit():
    if should_exit:
        log_print("✅ 程序已退出。")
        sys.exit(0)

# ========== 日志系统 ==========
def setup_logging():
    """创建日志文件夹和文件"""
    # 获取当前日期作为文件夹名
    today = datetime.now().strftime('%Y-%m-%d')
    
    # exe 所在目录
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(__file__)
    
    # 创建日志文件夹
    log_folder = os.path.join(base_dir, today)
    os.makedirs(log_folder, exist_ok=True)
    
    # 创建日志文件（带时间戳）
    timestamp = datetime.now().strftime('%H-%M-%S')
    log_file = os.path.join(log_folder, f'log_{timestamp}.txt')
    
    return log_file

# 初始化日志文件
LOG_FILE = setup_logging()

def log_print(message):
    """同时输出到控制台和日志文件"""
    print(message)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"写入日志失败: {e}")

# ========== 加载配置文件 ==========
def load_config():
    # config.json 和图片都和 exe 在同一目录
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    
    config_path = os.path.join(base_path, 'config.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config, base_path
    except FileNotFoundError:
        log_print(f"❌ 找不到配置文件: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        log_print(f"❌ 配置文件格式错误: {e}")
        sys.exit(1)

def parse_image_config(config_value, base_path):
    """解析配置项，返回 (图片路径, confidence)"""
    if isinstance(config_value, str):
        parts = config_value.strip().split()
        if len(parts) == 2:
            img_name, confidence = parts
            return os.path.join(base_path, img_name), float(confidence)
        else:
            # 如果只有文件名，使用默认 confidence
            return os.path.join(base_path, config_value.strip()), 0.8
    return None, 0.8

# 加载配置
config, base_path = load_config()

# 解析 bug 图片列表
bug_configs = []
for bug_config in config.get('bug', []):
    img_path, confidence = parse_image_config(bug_config, base_path)
    if img_path:
        bug_configs.append({'path': img_path, 'confidence': confidence})

# 解析其他图片
img_whistle, conf_whistle = parse_image_config(config.get('whistle', 'whistle.png 0.8'), base_path)
img_ball, conf_ball = parse_image_config(config.get('ball', 'ball.png 0.8'), base_path)
img_turn, conf_turn = parse_image_config(config.get('turn', 'turn.png 0.9'), base_path)
img_beetle, conf_beetle = parse_image_config(config.get('beetle', 'beetle.png 0.8'), base_path)
img_candy, conf_candy = parse_image_config(config.get('candy', 'candy.png 0.8'), base_path)
img_war, conf_war = parse_image_config(config.get('war', 'war.png 0.85'), base_path)

log_print(f"✅ 配置加载成功，找到 {len(bug_configs)} 个虫子图片")
log_print(f"📁 日志文件: {LOG_FILE}")

# ========== 程序开始 ==========
log_print("欢迎使用圆宇懒惰虫助手！可以随时按下 Esc 键退出程序。")
use_candy_input = input("是否使用甜食？y/n ")
use_candy = use_candy_input.strip().lower() == 'y'
log_print(f"甜食选项: {'是' if use_candy else '否'}")

log_print("程序将在 5 秒后开始运行，请切换到目标窗口...")
time.sleep(5)
log_print("程序开始运行!")

check_exit()

def wait_for_image(image_path, confidence=0.8, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        check_exit()
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                return location
        except:
            pass
        time.sleep(0.5)
    return None

while True:  # 主循环
    check_exit()
    log_print("\n🔁 开始新一轮")
    candy_used = False
    log_print("等待哨子出现...")
    if not wait_for_image(img_whistle, conf_whistle, timeout=60):
        log_print("⚠️ 未检测到哨子，重试...")
        continue

    # 如果需要甜食，而且还没点过，就尝试点击甜食
    if use_candy and not candy_used:
        log_print("🔍 检查是否有甜食...")
        try:
            candy_location = pyautogui.locateOnScreen(img_candy, confidence=conf_candy)
            if candy_location:
                pyautogui.click(pyautogui.center(candy_location))
                log_print("🍬 点击了甜食")
                candy_used = True
                time.sleep(0.5)
            else:
                log_print("⚠️ 没有找到甜食图标")
        except:
            pass

    log_print("✅ 检测到哨子，开始找虫...")
    clicked_bug = False

    while not clicked_bug:  # 一直找，直到进战斗
        check_exit()

        # 先全程监控 war（防止延迟进入战斗）
        try:
            war_location = pyautogui.locateOnScreen(img_war, confidence=conf_war)
            if war_location:
                log_print("⚔️ 检测到 war（延迟出现），进入战斗")
                clicked_bug = True
                break
        except:
            pass

        for bug_config in bug_configs:
            check_exit()
            try:
                bug_location = pyautogui.locateOnScreen(bug_config['path'], confidence=bug_config['confidence'])
                if bug_location:
                    center = pyautogui.center(bug_location)
                    pyautogui.click(center)
                    log_print(f"点击了 {os.path.basename(bug_config['path'])}，检测是否进入战斗...")

                    # 等 6 秒检测 war
                    start_time = time.time()
                    while time.time() - start_time < 6:
                        check_exit()
                        try:
                            if pyautogui.locateOnScreen(img_war, confidence=conf_war):
                                log_print("⚔️ 检测到 war，进入战斗")
                                clicked_bug = True
                                break
                        except:
                            pass
                        time.sleep(0.1)

                    if clicked_bug:
                        break  # 退出 bug 循环
                    else:
                        log_print("❌ 6 秒内没检测到 war，继续找虫...")
            except Exception as e:
                log_print(f"检测虫子时出现异常: {e}")
                continue

        if not clicked_bug:
            try:
                war_location = pyautogui.locateOnScreen(img_war, confidence=conf_war)
                if war_location:
                    log_print("⚔️ 检测到 war（延迟出现），进入战斗")
                    clicked_bug = True
                    break
            except:
                pass

            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width / 2, screen_height / 2)
            log_print("🎯 点击了屏幕中央")
            try:
                whistle_location = pyautogui.locateOnScreen(img_whistle, confidence=conf_whistle)
                if whistle_location:
                    pyautogui.click(pyautogui.center(whistle_location))
                    log_print("👉 点击了哨子")
            except:
                pass

    log_print("开始寻找独角仙及监听 '轮到你了' 状态...")

    turn_count = 0
    beetle_found = False
    start_time = time.time()

    # 检测是否有独角仙
    while True:
        check_exit()
        if time.time() - start_time > 20:
            log_print("⏱ 超过 20 秒没有轮到我，返回找虫")
            break
        
        # 先查独角仙
        try:
            if pyautogui.locateOnScreen(img_beetle, confidence=conf_beetle):
                log_print("✅ 检测到独角仙，进入独角仙流程")
                beetle_found = True
                break
        except:
            pass

        # 查turn计数
        try:
            if pyautogui.locateOnScreen(img_turn, confidence=conf_turn):
                log_print(f"❗️ 检测到第 {turn_count + 1} 次 '轮到你了'")
                turn_count += 1
                start_time = time.time()
                if not beetle_found:
                    if turn_count == 1:
                        pyautogui.press('up', presses=38)
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
                        log_print("❗️ 第三次turn，无独角仙，执行一次按键动作")
                        pyautogui.press('x')
                        pyautogui.keyDown('space')
                        time.sleep(4)
                        pyautogui.keyUp('space')
                        log_print("第三次turn动作完成，直接跳出战斗循环，开始新一轮")
                        break

                # 等待turn消失，避免多次计数
                while True:
                    check_exit()
                    try:
                        if not pyautogui.locateOnScreen(img_turn, confidence=conf_turn):
                            break
                    except:
                        break
                    time.sleep(0.2)
        except:
            pass

    # 如果检测到独角仙，执行正常独角仙攻击流程
    if beetle_found:
        log_print("✅ 进入独角仙攻击流程")
        pyautogui.press('up', presses=17)

        turn_count = 0
        log_print("等待出现三次 '轮到你了'...")
        while turn_count < 3:
            check_exit()
            try:
                if pyautogui.locateOnScreen(img_turn, confidence=conf_turn):
                    turn_count += 1
                    start_time = time.time()
                    log_print(f"第 {turn_count} 次检测到 '轮到你了'")
                    if turn_count == 1:
                        log_print("🔹 第一次攻击：按 1 2 后蓄力")
                        pyautogui.press(['1', '2'])
                        time.sleep(0.2)
                        pyautogui.keyDown('space')
                        time.sleep(2.6)
                        pyautogui.keyUp('space')
                    elif turn_count == 2:
                        log_print("🔹 第二次攻击：按 Z 后蓄力")
                        pyautogui.press('z')
                        time.sleep(0.5)
                        pyautogui.keyDown('space')
                        time.sleep(2.6)
                        pyautogui.keyUp('space')
                    elif turn_count == 3:
                        pyautogui.press('up', presses=21)
                        log_print("🔹 第三次攻击：按 X 后蓄力")
                        pyautogui.press('x')
                        pyautogui.keyDown('space')
                        time.sleep(4)
                        pyautogui.keyUp('space')

                    # 等待 "轮到你了" 消失
                    while True:
                        check_exit()
                        try:
                            if not pyautogui.locateOnScreen(img_turn, confidence=conf_turn):
                                break
                        except:
                            break
                        time.sleep(0.5)
            except:
                pass
            time.sleep(0.2)

        log_print("🔄 独角仙战斗完成，等待哨子出现...")