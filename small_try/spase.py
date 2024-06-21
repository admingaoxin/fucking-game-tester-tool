# import pyautogui
# import time
# import random                                                                     
# while True:
#     pyautogui.press('space')
#     time.sleep(0.1)
#     pyautogui.keyDown(random.choice(['w','a','s','d'])) 
    # pyautogui.press(random.choice(['up','left','right','down']))




# import pyautogui
# import random
# import time

# while True:
#     pyautogui.press('space')
#     pyautogui.press('space')
#     time.sleep(2)
#     direction = random.choice(['w', 'a', 's', 'd'])
#     pyautogui.press(direction)



# import pyautogui
# import time 
# import random
# import win32api


# while True:
#     print(pyautogui.position())
#     win = device('arkgame')
#     x, y = win32api.GetCursorPos()
#     win.mouse_move((x+10, y+10))
#     win.mouse_down('right')
#     # ...  // some operations
#     win.mouse_up('right')
#     # pyautogui.PAUSE = 0

#     # pyautogui.moveTo(x=1500, y=random.randint(100, 900))
#     # time.sleep(0.2)
#     pyautogui.press('space') 
#     pyautogui.press('space')
#     # time.sleep(0.1)
#     # pyautogui.moveTo(y=1500, x=random.randint(100, 900))
#     key = random.choice(['w', 'a', 's', 'd'])
#     pyautogui.keyDown(key)
#     time.sleep(1)
            

# import pyautogui
# import time 
# import random
# import win32api
# import win32con 
# import pywinauto
# # 获取屏幕大小
# # screenWidth, screenHeight = pyautogui.size()
# # 移动鼠标到屏幕中央
# # pyautogui.moveTo(screenWidth / 2, screenHeight / 2, duration = 1.5)
# while True:
#     print(pyautogui.position())
   

#     # pyautogui.dragTo(200, 200, duration=0.5)  # 拖动到目标位置
#     # sizex,sizey=pyautogui.size()
#     # pyautogui.moveTo(sizex/2,sizey/2,duration=1)
#     # pyautogui.moveRel(100, -200, duration=0.2)
    
#     x, y = win32api.GetCursorPos()
#     win32api.SetCursorPos((x+10, y+10))
#      # 使用pywinauto移动鼠标往右200像素
#     app = pywinauto.Application().connect(title_re=".*")
#     app_dialog = app.top_window()
#     app_dialog.MoveWindow(x+200, y, 100, 100, True)
#     # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x+1000, y+0, 0, 0)
#     time.sleep(0.1)
#     # # ...  // some operations
#     # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x+1000, y+0, 0, 0)

#     pyautogui.PAUSE = 0

#     # pyautogui.moveTo(x=1500, y=random.randint(100, 900))
#     key = random.choice(['w', 'a', 's', 'd'])
#     pyautogui.keyDown(key)  
#     time.sleep(1) 
#     pyautogui.press('space')
#     time.sleep(0.1) 
#     pyautogui.press('space')
#     time.sleep(0.1)
#     # pyautogui.moveTo(y=1500, x=random.randint(100, 900))
    
#     pyautogui.keyUp(key) 
#     time.sleep(0.5)


# import pyautogui
# import time 
# import random
# import win32api
# import win32con 
# import pywinauto
# from pywinauto import mouse
# # sb = 0
# # x, y = pyautogui.position()
# # while sb < 3000:
# #     mouse.move(coords=(x+1, y))
# #     print(pyautogui.position())


# # Use pywinauto to get the arkgame process
# app = pywinauto.Application().connect(title_re="SYNCED")
# screenWidth, screenHeight = pyautogui.size()
# # Set a global pause for pyautogui
# pyautogui.PAUSE = 0

# while True: 
#     print(pyautogui.posi
#     key = random.choice(['w', 'a', 's', 'd'])
#     pyautogui.keyDown(key)
#     pyautogui.press('space', pressesw  
# #     time.sleep(1) 
# #     pyautogui.press('space')
# #     time.sleep(0.1) 
# #     pyautogui.press('space')
# #     time.sleep(0.1)
    
# #     pyautogui.keyUp(key) 
# #     time.sleep(0.5)


import pyautogui
import time 
import random
import win32api
import win32con 
import pywinauto
# import airtest
from pywinauto import mouse
# 使用pywinauto获取arkgame进程
app = pywinauto.Application().connect(title_re="SYNCED")

while True:
    print(pyautogui.position())
    # 获取当前鼠标位置
    x, y = win32api.GetCursorPos()
    # win.mouse_move((x+10, y+10))
    # 往右移动200像素
    # x += 200 
    # 移动鼠标
    mouse.move(coords=(x, y))
    x, y = win32api.GetCursorPos()
    win32api.SetCursorPos((x+10, y+10))

    # # 使用pywinauto移动鼠标往右200像素
    # app_dialog = app.top_window()
    # app_dialog.MoveWindow(x+200, y, 100, 100, True)

    pyautogui.PAUSE = 0

    key = random.choice(['w', 'a', 's', 'd'])
    pyautogui.keyDown(key)  
    time.sleep(1) 
    pyautogui.press('space')
    time.sleep(0.1) 
    pyautogui.press('space')
    time.sleep(0.1)
    pyautogui.keyUp(key) 
    time.sleep(0.5)
    pyautogui.keyDown('space')
    time.sleep(5.0)
    pyautogui.keyUp('space')
    