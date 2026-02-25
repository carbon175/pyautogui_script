import pyautogui
import time
import keyboard


pyautogui.FAILSAFE=True
first_turn_detected = False
arrow_location = None
round_count =0

def shoot_when_power_reaches(target_image, timeout=5):
    """ 按住空格，直到目标力度条图片出现后松开 """
    print("开始蓄力...")
    pyautogui.keyDown('space')  # 按住空格
    start_time = time.time()

    while True:
        try:
            power_location = pyautogui.locateOnScreen(target_image, confidence=0.9)
            if power_location:
                print(f"{target_image} 出现，松开空格！")
                pyautogui.keyUp('space')  # 松开空格
                return True
        except pyautogui.ImageNotFoundException:
            pass  # 忽略异常，继续循环

        if time.time() - start_time > timeout:
            print("超时未检测到目标力度，松开空格")
            pyautogui.keyUp('space')  # 超时后强制松开
            return False

        time.sleep(0.01)  # 缩短检测间隔，提高识别精度

def wait_for_appear(image, timeout=10, confidence=0.9):
    """等待图像出现，避免 ImageNotFoundException"""
    print(f"正在等待 {image} 出现...")
    start_time = time.time()

    while True:
        
        try:
            if keyboard.is_pressed('esc'):  # 检测是否按下 Esc 退出
             print("检测到退出键，停止脚本！")
             return None

            location = pyautogui.locateOnScreen(image, confidence=confidence)
            if location:
                print(f"检测到 {image}，坐标：{location}")
                return location
        except pyautogui.ImageNotFoundException:
            pass  # 忽略异常，继续等待
        
        # 超时机制
        if time.time() - start_time > timeout:
            print(f"超时 {timeout} 秒，未找到 {image}")
            return None
        
        time.sleep(0.5)  # 每 0.5s 检测一次
        return None

#def drag_scroll():
    """按住滚动条并向下拖动"""
    #scroll_location = wait_for_appear("scroll.png")  # 查找滚动条
    #if scroll_location:
     #   pyautogui.moveTo(scroll_location)  # 移动到滚动条
    #    pyautogui.mouseDown()  # 按住鼠标左键
    #    pyautogui.moveRel(0, 300, duration=0.5)  # 向下拖拽300像素
    #    pyautogui.mouseUp()  # 释放鼠标左键
    #    print("拖动滚动条完成")
   # else:
   #     print("未找到滚动条")
    
def wait_for_power(timeout=1.5, confidence=0.6):
    """在指定时间内持续查找 power.png，找到就返回 True，否则 False"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        power_location = wait_for_appear('power.png', confidence=confidence)
        if power_location:
            return power_location
        time.sleep(0.1)  # 小间隔，避免CPU占用过高
    return None


def click_button_when_appears(image):
    """等待按钮出现后点击，找不到则尝试拖动滚动条"""
    
    location = wait_for_appear(image)  # 先等按钮出现
    if location:
        center = pyautogui.center(location)  # 确保点击中心
        pyautogui.moveTo(center, duration=0.2)  # 移动鼠标到目标
        pyautogui.click(center, duration=0.2)  # 缓慢点击，确保生效
        print(f"点击了 {image}，位置：{center}")
        return  # 成功点击后退出函数

    print(f"未找到 {image}，尝试拖动滚动条")
   # drag_scroll()  # 调用拖动滚动条函数

    time.sleep(1)  # 等待 UI 更新

    # 再次尝试查找按钮
    location = wait_for_appear(image)
    if location:
        center = pyautogui.center(location)  # 确保点击中心
        pyautogui.moveTo(center, duration=0.2)
        pyautogui.mouseDown(center)
        time.sleep(0.1)  # 停顿 0.1s
        pyautogui.mouseUp(center)
        print(f"滚动后点击了 {image}，位置：{center}")
    else:
        print(f"滚动后仍未找到 {image}，跳过")

time.sleep(3)  



print("检测 dragon_nose.png 是否存在...")
time.sleep(2)  # 稍等 1 秒，确保 redbutton 点击完成

# 计算屏幕中心

def find_dragon():

    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    # 初始偏移量（右 + 上）
    offset_x = 100  # 右移 100 像素
    offset_y = -50  # 上移 50 像素

    # 增量（每次点击向右上方移动）
    increment_x = 100  # 每次点击后右移 20 像素
    increment_y = -40  # 每次点击后上移 10 像素

    # 计算目标点击位置
    target_x = center_x + offset_x
    target_y = center_y + offset_y

    # 添加计数器
    click_count = 0
    max_clicks = 4
    arrow_location = None
    arrowBoss_location = wait_for_appear('arrow_boss.png', confidence=0.8)
    pyautogui.moveTo(arrowBoss_location)
    center = pyautogui.center(arrowBoss_location)  # 确保点击中心
    pyautogui.moveTo(center, duration=0.2)
    pyautogui.mouseDown(center)
    time.sleep(0.3)  # 停顿 0.1s
    pyautogui.mouseUp(center)

    # 循环检测 `dragon_nose.png`，如果不存在就不断点击目标区域
    while click_count < max_clicks:
        try:
            nose_location = pyautogui.locateOnScreen('dragon_nose.png', confidence=0.8, grayscale=True)
            
            if nose_location is not None:  # 只有找到图片才点击
                center = pyautogui.center(nose_location)  # 确保点击中心
                pyautogui.moveTo(center, duration=0.2)
                pyautogui.mouseDown(center)
                time.sleep(0.1)  # 停顿 0.1s
                pyautogui.mouseUp(center)
                pyautogui.click(center,clicks=3)
                print("检测到 dragon_nose.png，点击完成！")
                break  # 找到并点击后应该退出循环
            else:
                pyautogui.click(target_x, target_y)
                print(f"dragon_nose.png 不存在，点击屏幕 ({target_x}, {target_y})，第 {click_count + 1} 次点击")

                # 计算新的目标位置（向右上方移动）
                target_x += increment_x
                target_y += increment_y
                time.sleep(1)
                click_count += 1
            
        
        except pyautogui.ImageNotFoundException:
            pyautogui.click(target_x, target_y)
            print(f"dragon_nose.png 不存在，点击屏幕 ({target_x}, {target_y})，第 {click_count + 1} 次点击")

            # 计算新的目标位置（向右上方移动）
            target_x += increment_x
            target_y += increment_y
            click_count += 1
            time.sleep(1.5)

# 查找并点击箭头
find_dragon()

while arrow_location is None:
   
    print("等待 arrow.png 出现...")
    arrow_location = wait_for_appear('arrow.png', confidence=0.9)
    
    if arrow_location:
            print("第一次检测到 arrow.png，按下 'right' 键")
            time.sleep(0.5)
            pyautogui.press('up',presses=22)
            pyautogui.click(arrow_location)
            
    else:
        ('waiting for arrow')

while True:
            print("等待 turn.png 出现...")
        
        # **检测是否死亡**
            try:
                die_location = pyautogui.locateOnScreen('die.png', confidence=0.8)
            except pyautogui.ImageNotFoundException:
                die_location = None  # 如果找不到 die.png，就设置为空

            if die_location:
                print("检测到 die.png，执行回退操作...")
                first_turn_detected = False  # 重新标记未检测到 turn.png
                arrow_location=None
                round_count = 0  # 重新计数
                click_count = 0

                for image in ['back.png', 'confirm.png']:
                    click_button_when_appears(image)
                    time.sleep(0.5)  # 避免连点
                    
                time.sleep(14)
                click_button_when_appears('redbutton.png')
                find_dragon()

                continue  # 重新开始流程，等待 turn.png
            

            # **等待 turn.png 出现**
            turn_location = wait_for_appear('turn.png', confidence=0.8)
            power_location = wait_for_appear('power.png',confidence=0.6)
            if turn_location:
                round_count += 1
                print(f"当前回合: {round_count}")

                power_location = wait_for_power(timeout=1.5, confidence=0.6)

                keys = []  # 存放本回合要按的键

                if round_count == 1:
                    # 第1回合：先按 right + 124
                    keys = ['right', '1', '2', '4']

                elif round_count < 3:
                    # 第2回合
                    if power_location:
                        keys = ['3', '3', '4', 'b']  # 334b
                    else:
                        keys = ['1', '2', '4']       # 124

                else:
                    # 第3回合及以后
                    keys = ['q', 'z', 'x', 'c', '1', '2', '4']
                    if power_location:
                        keys.extend(['3', '3', '4', 'b'])
                    else:
                        keys.extend(['q', 'z', 'x', 'c', '1', '2', '4'])

                # 执行按键
                for key in keys:
                    pyautogui.press(key)
                    time.sleep(0.1)

                # 每个回合最后都要做力度条检测（自动按/松开 space）
                print("执行力度条检测 (shoot)")
                shoot_when_power_reaches('power_bar_55.png')

            else:
                print("未检测到 turn.png，继续等待...")

            print("所有按钮已点击完毕！")
