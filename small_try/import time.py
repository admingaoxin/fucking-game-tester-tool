from ahk import AHK 
ahk = AHK 
import pyautogui
import win32api
import time

pyahk = ahk.script()
# 创建AHK对象
while True:
    
    print(pyautogui.position())
    x, y = win32api.GetCursorPos()
    # 移动鼠标到(x,y)坐标
    pyahk.mouse_move(x+10, y+10)
    time.sleep(2)
    pyahk.mouse_move(200, 200, speed=2)


