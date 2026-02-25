import pyautogui
import time
import keyboard

time.sleep(3)
pyautogui.FAILSAFE=True

def wait_for_appear(image, timeout=20, confidence=0.9,):
    """等待图像出现，避免 ImageNotFoundException"""
    print(f"正在等待 {image} 出现...")
    start_time = time.time()

    while True:

        try:
            if keyboard.is_pressed('c'):  # 检测是否按下 Esc 退出
             print("检测到退出键，停止脚本！")
             return None

            location = pyautogui.locateOnScreen(image, confidence=confidence,grayscale=True)
            if location:
                print(f"检测到 {image}，坐标：{location}")
                return location
        except pyautogui.ImageNotFoundException:
            pass  # 忽略异常，继续等待

        # 超时机制
        if time.time() - start_time > timeout:
            print(f"超时 {timeout} 秒，未找到 {image}")
            return None

        time.sleep(1)  # 每 0.5s 检测一次
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

    time.sleep(3)  # 等待 UI 更新

    # 再次尝试查找按钮
    location = wait_for_appear(image)
    if location:
        center = pyautogui.center(location)  # 确保点击中心
        pyautogui.moveTo(center, duration=0.2)
        pyautogui.mouseDown(center)
        time.sleep(0.5)  # 停顿 0.1s
        pyautogui.mouseUp(center) 
        print(f"滚动后点击了 {image}，位置：{center}")
    else:
        print(f"滚动后仍未找到 {image}，跳过")

for image in ['shop.png', 'xunzhang.png', 'daoju.png', 'right.png', 'card.png', 'buy.png', 'confirm_buy.png', 'horse.png', 'ide.png','tick.png', 'mount_upgrade.png','mount_upgrade.png','mount_skill.png','small_upgrade.png','jineng_upgrade.png','jineng_upgrade.png','jineng_upgrade.png','jineng_upgrade.png','jineng_upgrade.png','close.png','door.png','pet.png','peiyang.png','jinhua.png','red_jinhua.png','red_jinhua.png','red_jinhua.png','red_jinhua.png','red_jinhua.png','jinhua_close.png','close.png','jingcai.png','cangbao.png','back.png','bizuo.png','zhuangyuan.png','niudan.png','niu.png','close.png','door.png','bizuo.png','lingqu.png','mijing.png','mohuan.png','tiaozhan.png','off.png','confirm.png','hand.png','yanyu.png','dun.png','like.png']:
    click_button_when_appears(image)
    time.sleep(1.5)  # 避免连点