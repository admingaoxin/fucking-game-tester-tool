import win32gui
import win32api
while True:
    hwnd = win32gui.GetForegroundWindow()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win32api.SetCursorPos((left + 50, top + 50))