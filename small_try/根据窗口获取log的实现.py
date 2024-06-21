import os
import win32gui
import psutil
import win32process
#获取当前所有的活动窗口
def get_window_handle(title):
    def callback(handle, data):
        if title in win32gui.GetWindowText(handle):
            window_handles.append(handle)
    
    window_handles = []
    win32gui.EnumWindows(callback, None)

    if len(window_handles) > 0:
        return window_handles[0]
    else:
        return None
#要传进去的几个东西。
window_title = "SYNCED"
folder_path = "\Saved\Logs"
to_remove = '\Binaries\Win64\SYNCED-Win64-Development.exe'
#获取指定的活动窗口
handle = get_window_handle(window_title)
if handle is not None:
    pid = win32process.GetWindowThreadProcessId(handle)[1]
    p = psutil.Process(pid)
    #根据当前活动窗口获得它的路径
    exe_path = p.exe()
    # folder_path = os.path.join(os.path.dirname(exe_path), folder_path)这段路径拼接注释掉，是根据当前的路径获取，不删，后面可能有用
    print(exe_path)
    #路径拼接~
    base_path =exe_path.split(to_remove)[0]
    print(base_path)
    new_path = os.path.join(base_path+folder_path)
    #打开路径
    os.startfile(new_path)
    print(new_path)
else:
    print("Window not found.")

# try:
#     window_title = "Notepad"
#     folder_path = "my_folder"

#     open_exe_path(window_title, folder_path)
# except Exception as e:
#     print(f"An error occurred: {e}")

