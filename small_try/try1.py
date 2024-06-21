import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time
from datetime import datetime
from PIL import ImageGrab, ImageDraw
import numpy as np
import cv2
import pygetwindow as gw
import os
import pyautogui as pag
from pytest import param
import win32gui
import psutil
import win32process
import ctypes
from ctypes import wintypes
import win32con
VIDEO_FILE_PATH = '\\record_files'
FPS = 5.2
MAX_FILES_COUNT = 100
dir_name = '\\record_files'
proc_name = "Ld9BoxHeadless.exe"

def recode(window_title='Warframe'):
    # 1.首先根据窗口名称获取到对应的窗口
    window = gw.getWindowsWithTitle('debug包')[0]
    # 2.激活并将对应的窗口显示到最顶层
    window.restore()
    window.activate()
    # 3.根据当前时间生成录像文件的名字
    file_name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    # 4.获取窗口的位置和大小
    left, top, width, height = window.left, window.top, window.width, window.height
    # 5.设置VideoWriter_fourcc录制类型
    fourcc = cv2.VideoWriter_fourcc(*'WMV1')
    # 6.设置文件名，大小，帧率等， VIDEO_FILE_PATH一个全局参数，是录像的保存目录，如VIDEO_FILE_PATH = 'E:\\record_files'
    #   FPS这个地方有点问题，后面考虑怎么细化这个东西FPS=15，这个帧率可能会影响录像的播放速度，可以根据自己的情况自行调整
    video = cv2.VideoWriter(f'{VIDEO_FILE_PATH}\\{file_name}.wmv', fourcc, FPS, (width, height))
    # 7.记录开始录制视频的时间
    start_time = time.time()
    # 8.当录制时间不足xx分钟时，循环写入到录像文件中
    while time.time() - start_time < 60:
        # 这里我每次写入都重新获取了窗口的顶点位置和大小，这样的用处是在你拖动对应的窗口后，录像的区域会跟随你的拖动重新选定，不会傻傻的还在录原来的位置
        left, top, width, height = window.left, window.top, window.width, window.height
        # 根据窗口区域截取对应的图像
        capture_image = ImageGrab.grab((left, top, left+width, top+height))
        # 生成图像帧
        frame = cv2.cvtColor(np.array(capture_image), cv2.COLOR_RGB2BGR)
        # 将图像帧写入到文件中
        video.write(frame)
    video.release()
def del_files():
    """
    判断文件数量是否超过设定值，如果超过，则删除一定数量的文件
    :return:
    """
    # 根据目录获取文件列表
    files = os.listdir(VIDEO_FILE_PATH)
    # 判断文件数量，如果超过了设定的最大值MAX_FILES_COUNT（自行定义），则删除最前面的几个文件
    if len(files) > MAX_FILES_COUNT:
        for i in files[:len(files)-MAX_FILES_COUNT]:
            os.remove(f'{VIDEO_FILE_PATH}\\{i}')
    # elif len(files) < 1:
    #     os.path.join('x.txt')
    #     with open(VIDEO_FILE_PATH, 'w') as f:
    #         f.write('Hello World!') 注掉，会报错，权限问题：[Errno 13] Permission denied: 'E:\record_files'

class WorkThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent)
        self.working = True
        
    def run(self):
        print("Running...启动时请用管理员模式启动，用户模式有概率不会生成视频文件")
        print('文件存放位置为:\\record_files（也就是这个文件所在位置的根目录，比如c盘，则是c：\\record_files）')
        #判断下目录下方是否有这个文件夹
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print('Directory', dir_name, 'created.')
        else:
            print('Directory', dir_name, 'already exists.')# 执行代码
        while self.working:
            
            try:                       
                while True:                                                
                        del_files()
                        recode('Warframe')
                        
                        self.signal.emit("成功\n")
            except Exception as e:
                self.signal.emit("失败：%s\n" % str(e))
    
    def stop(self):
        self.working = False

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('行车记录仪')
        self.setGeometry(100, 100, 500, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 按钮
        self.btn = QPushButton('开始执行', self.central_widget)
        self.btn.setGeometry(20, 20, 100, 30)
        self.btn.clicked.connect(self.on_btn_clicked)
        self.is_running = False
        # # 按钮2 - 执行一次
        # self.btn_once = QPushButton('打开log路径', self.central_widget)
        # self.btn_once.setGeometry(140, 20, 100, 30)
        # self.btn_once.clicked.connect(self.on_btn_once_clicked)
        # 按钮3 -
        self.btn_code = QPushButton('转储dump', self.central_widget)
        self.btn_code.setGeometry(260, 20, 120, 30)
        self.btn_code.clicked.connect(self.on_btn_code_clicked)
      
        # 文本框
        self.edit = QTextEdit(self.central_widget)
        self.edit.setGeometry(20, 60, 460, 400)

    def on_btn_clicked(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.btn.setText('停止执行')
            self.thread = WorkThread()
            self.thread.signal.connect(self.on_output_changed)

            # 重定向输出流
            sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
            self.thread.start()
        else:
            self.btn.setText('开始执行')
            self.thread.stop()
    #打开log路径的代码存放地址        
    def on_btn_once_clicked(self):
        
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
        # self.thread = WorkThread()
        # self.thread.signal.connect(self.on_output_changed)
    def on_btn_code_clicked(self):
        # 获取所有进程信息
        for proc in psutil.process_iter():
            try:
                if proc.name() == proc_name:
                    pid = proc.pid  # 如果名称匹配，则获取该进程ID
                    print("进程名称: ", proc_name, "PID: ", pid)
                # else : 
                #     print("找不到进程")
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            #     pinfo = proc.as_dict(attrs=['pid', 'name'])

            #     # 打印进程PID和名称
            #     print(pinfo['pid'], pinfo['name'])
            # except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            #     pass
        # 打开进程 SYNCED-Win64-Development.exe
        PROCESS_ALL_ACCESS = 0x1F0FFF
        process_id = pid
        print(process_id)
        print("dump文件存放位置与此exe存放位置一致")
        # process_id = 30440  # 替换为你要转储的进程ID
        kernel32_dll = ctypes.WinDLL('kernel32', use_last_error=True)
        process_handle = kernel32_dll.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)

        # 使用miniDumpWriteDump函数进行转储操作
        dbghelp_dll = ctypes.WinDLL('Dbghelp.dll', use_last_error=True)
        filename = 'synced.dmp'  # 转储文件的名称
        handle = kernel32_dll.CreateFileW(
            filename,
            0x10000000,  # GENERIC_WRITE
            0,
            None,
            2,  # CREATE_ALWAYS
            0,
            None
        )
        MINIDUMP_TYPE = ctypes.c_int
        MiniDumpWithFullMemory = 2
        dump_flags = MINIDUMP_TYPE(MiniDumpWithFullMemory)
        dbghelp_dll.MiniDumpWriteDump(
            process_handle,
            process_id,
            handle,
            dump_flags,
            None,
            None,
            None
        )

        # 关闭相关句柄和资源
        kernel32_dll.CloseHandle(handle)
        kernel32_dll.CloseHandle(process_handle)

        self.thread = WorkThread()
        self.thread.signal.connect(self.on_output_changed)


    def normalOutputWritten(self, text):
        cursor = self.edit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.edit.setTextCursor(cursor)
        self.edit.ensureCursorVisible()

    def on_output_changed(self, text):
        self.edit.insertPlainText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
