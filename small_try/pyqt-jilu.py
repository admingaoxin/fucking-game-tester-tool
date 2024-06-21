import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QThread, QTimer
import time
from datetime import datetime
from PIL import ImageGrab, ImageDraw
import numpy as np
import cv2
import pygetwindow as gw
import os
import pyautogui as pag
from pytest import param
VIDEO_FILE_PATH = 'E:\\record_files'
FPS = 5
MAX_FILES_COUNT = 30
dir_name = 'E:\\record_files'
print('有bug烦请联系ratangao 初版demo 欢迎试用提出问题.jpg')  
#判断下目录下方是否有这个文件夹
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    print('Directory', dir_name, 'created.')
else:
    print('Directory', dir_name, 'already exists.')

def recode(window_title='SYNCED'):
# 1.首先根据窗口名称获取到对应的窗口
    window = gw.getWindowsWithTitle('SYNCED')[0]
    # 2.激活并将对应的窗口显示到最顶层
    window.restore()
    window.activate()
    # 3.根据当前时间生成录像文件的名字
    file_name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    # 4.获取窗口的位置和大小
    left, top, width, height = window.left, window.top, window.width, window.height
    # 5.设置VideoWriter_fourcc录制类型
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # 6.设置文件名，大小，帧率等， VIDEO_FILE_PATH一个全局参数，是录像的保存目录，如VIDEO_FILE_PATH = 'E:\\record_files'
    #   FPS这个地方有点问题，后面考虑怎么细化这个东西FPS=15，这个帧率可能会影响录像的播放速度，可以根据自己的情况自行调整
    video = cv2.VideoWriter(f'{VIDEO_FILE_PATH}\\{file_name}.AVI', fourcc, FPS, (width, height))
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
# if __name__ == '__main__':
#     main()

class MyThread(QThread):
    
                   
    def __init__(self):
        super().__init__()

    def run(self):
        # 在这里写你的代码
        while True:
            del_files()
            recode('SYNCED')      
            print("Running...")
            self.sleep(1)
            
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button example - Genie'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 创建按钮并绑定事件
        self.button = QPushButton('开始运行', self)
        self.button.setToolTip('点击此按钮开始')
        self.button.move(100, 70)
        self.button.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        # 创建线程并启动
        if self.button.text() == "开始运行":
            self.button.setText("停止")
            self.thread = MyThread()
            self.thread.start()
        else:
            self.button.setText("开始运行")
            self.thread.terminate()  # 停止线程

    def closeEvent(self, event):
        # 关闭窗口时结束线程
        reply = QMessageBox.question(self, 'Message',
                                    "确定要退出吗？", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.thread.terminate()
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
