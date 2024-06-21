import psutil
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
import win32gui
# 设置录制的帧率和时长
FPS = 15
DURATION = 30

class Recorder(QWidget):
    def __init__(self, process_name):
        super().__init__()
        self.process_name = process_name
        self.process = None
        self.hwnd = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.frames = []
        self.current_frame = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Recorder")
        self.setGeometry(100, 100, 640, 480)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def start_recording(self):
        # 获取进程信息和主窗口句柄
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.process_name:
                self.process = proc
                break
        else:
            raise ValueError(f"No process found with name {self.process_name}")
        self.hwnd = self.process.as_dict(attrs=['pid', 'name', 'username', 'memory_info'])['pid']
        # 开始录制
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter('temp.avi', fourcc, FPS, (self.width(), self.height()))
        start_time = cv2.getTickCount()
        while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < DURATION:
            # 获取窗口截图
            img = self.get_window_image()
            # 将图像帧写入文件
            video.write(img)
            # 显示图像帧
            self.frames.append(img)
            self.current_frame = len(self.frames) - 1
            self.show_frame()
        video.release()
        # 开始定时器
        self.timer.start(1000 // FPS)

    def get_window_image(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
if __name__ == '__main__':
    main()