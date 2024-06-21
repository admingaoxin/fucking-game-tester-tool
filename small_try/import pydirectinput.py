import pydirectinput
import time
count = 0
while count < 20:
    # 移动鼠标到坐标点(100, 100)
    pydirectinput.move(xOffset=0, yOffset=10, relative=True)
    # moveSum -= 10

    # 点击鼠标左键
    pydirectinput.click()

    # 等待2秒钟
    time.sleep(1)

    # 移动鼠标到坐标点(200, 200)
    pydirectinput.move(xOffset=100, yOffset=10, relative=True)
    # moveSum -= 10

    # 点击鼠标右键
    pydirectinput.rightClick()
    count += 1
