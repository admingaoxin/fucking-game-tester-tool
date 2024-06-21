from concurrent.futures.thread import _worker
import sys
import psutil
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QComboBox, QPushButton, QSizePolicy
import win32gui
import win32con
import win32process
import os
import datetime as dt
import time
import cv2
import pygetwindow as gw
from PIL import ImageGrab, ImageDraw
import numpy as np
VIDEO_FILE_PATH = 'E:\\record_files'
FPS = 5
MAX_FILES_COUNT = 30
dir_name = 'E:\\record_files'
proc_name = "SYNCED-Win64-Development.exe"
folder_path = "\Saved\Logs"
to_remove = '\Binaries\Win64\SYNCED-Win64-Development.exe'

class WorkThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent)
        self.working = True
        
    def run(self):
        print("Running...")
        print('有bug烦请联系ratangao 初版demo 欢迎试用提出问题.jpg \n 文件存放位置为:E:\\record_files')
        #判断下目录下方是否有这个文件夹
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print('Directory', dir_name, 'created.')
        else:
            print('Directory', dir_name, 'already exists.')# 执行代码
        while self.working:
            
            try:                       
                while True:                                                
                        print('zzzz')
                        
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

    
        self.setWindowTitle('Process Manager')
        self.setGeometry(100, 100, 600, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # 添加标签和下拉框部件
        self.process_combobox = QComboBox(self)
        self.process_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.process_combobox.setFixedHeight(80) # 增加高度
        self.process_combobox.setFixedWidth(400)
        self.process_combobox.move(120, 30)
        self.process_combobox.currentTextChanged.connect(self.update_button_status)

        # 添加文本输出框和按钮部件
        self.text_output = QLabel(self)
        self.text_output.setWordWrap(True)
        self.text_output.setGeometry(20, 80, 560, 400)

        self.exec_btn1 = QPushButton('Button 1', self)
        self.exec_btn1.setToolTip('Execute custom code for Button 1')
        self.exec_btn1.move(20, 500)
        self.exec_btn1.clicked.connect(self.on_exec_btn1_clicked)
        self.exec_btn1.setEnabled(False)

        self.exec_btn2 = QPushButton('开始', self.central_widget)
        self.exec_btn2.setToolTip('Execute custom code for Button 2')
        self.exec_btn2.move(220, 500)
        self.exec_btn2.clicked.connect(self.on_exec_btn2_clicked)
        self.exec_btn2.setEnabled(False)

        self.exec_btn3 = QPushButton('Button 3', self)
        self.exec_btn3.setToolTip('Execute custom code for Button 3')
        self.exec_btn3.move(420, 500)
        self.exec_btn3.clicked.connect(self.on_exec_btn3_clicked)
        self.exec_btn3.setEnabled(False)
    
        # 添加关闭和最小化按钮部件
        self.close_button = QPushButton('Close', self)
        self.close_button.setToolTip('Close the selected process')
        self.close_button.move(20, 540)
        self.close_button.clicked.connect(self.on_close_button_clicked)
        self.close_button.setEnabled(False)

        self.minimize_button = QPushButton('minimize', self)
        self.minimize_button.setToolTip('Minimize the selected process')
        self.minimize_button.move(220, 540)
        self.minimize_button.clicked.connect(self.on_minimize_button_clicked)
        self.minimize_button.setEnabled(False)

        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.setToolTip('Refresh the process list')
        self.refresh_button.move(420, 540)
        self.refresh_button.clicked.connect(self.update_process_list)

        # 初始化界面数据
        self.update_process_list()
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

    # 更新进程列表
    def update_process_list(self):
        self.process_combobox.clear()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # 获取进程名和进程 ID
                pid = proc.info['pid']
                name = proc.info['name']
                self.process_combobox.addItem(f'{name} (PID: {pid})')
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

    # 关闭选定进程
    def on_close_button_clicked(self):
        selected_text = self.process_combobox.currentText()
        pid = int(selected_text.split(' (')[1].split(': ')[1][:-1])
        p = psutil.Process(pid)
        p.terminate()

    # MINIsize 
    def on_minimize_button_clicked(self):   
        selected_text = self.process_combobox.currentText()
        hwnd = int(selected_text.split(' (')[1].split(': ')[1][:-1])
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    # 按钮 1 执行代码
    def on_exec_btn1_clicked(self):  
        selected_text = self.process_combobox.currentText()
        pid = int(selected_text.split(' (')[1].split(': ')[1][:-1])
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

    # 按钮 2 执行代码
    def on_exec_btn2_clicked(self):
        if self.worker.running:
            self.worker.stop()
            self.exec_btn2.setText("Start")
        else:
            self.worker.start()
            self.exec_btn2.setText("Stop")

    def on_worker_finished(self):
        self.exec_btn2.setText("Start")

        # 1.首先根据窗口名称获取到对应的窗口
        window = gw.getWindowsWithTitle('SYNCED')[0]
        # 2.激活并将对应的窗口显示到最顶层
        window.restore()
        window.activate()
        # 3.根据当前时间生成录像文件的名字
        file_name = dt.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        # 4.获取窗口的位置和大小
        left, top, width, height = window.left, window.top, window.width, window.height
        # 5.设置VideoWriter_fourcc录制类型
        fourcc = cv2.VideoWriter_fourcc(*'WMV1')
        # 6.设置文件名，大小，帧率等， VIDEO_FILE_PATH一个全局参数，是录像的保存目录，如VIDEO_FILE_PATH = 'E:\\record_files'
        #   FPS这个地方有点问题，后面考虑怎么细化这个东西FPS=15，这个帧率可能会影响录像的播放速度，可以根据自己的情况自行调整
        video = cv2.VideoWriter(f'{VIDEO_FILE_PATH}\\{file_name}.WMV', fourcc, FPS, (width, height))
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
    # 按钮 3 执行代码
    def on_exec_btn3_clicked(self):
        code = "# Place your custom code for Button 3 here"
        result = eval(code)
        self.text_output.setText(str(result))

    # 更新按钮状态
    def update_button_status(self, text):
        if len(text) > 0:
            self.close_button.setEnabled(True)
            self.minimize_button.setEnabled(True)
            self.exec_btn1.setEnabled(True)
            self.exec_btn2.setEnabled(True)
            self.exec_btn3.setEnabled(True)
        else:
            self.close_button.setEnabled(False)
            self.minimize_button.setEnabled(False)
            self.exec_btn1.setEnabled(False)
            self.exec_btn2.setEnabled(False)
            self.exec_btn3.setEnabled(False)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
