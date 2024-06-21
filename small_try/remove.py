import pyautogui

# 开始录制
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
pyautogui.click(100, 100)
pyautogui.typewrite('Hello world!', interval=0.25)
pyautogui.hotkey('ctrl', 'd')

# 结束录制并生成脚本
pyautogui.displayMousePosition()
pyautogui.displayKeyboardMapping()
pyautogui.confirm('录制完成，生成脚本？')
pyautogui.write('script.py')
pyautogui.press('enter')
pyautogui.press('enter')