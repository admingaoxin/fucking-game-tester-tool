
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
FPS = 7
MAX_FILES_COUNT = 10
dir_name = 'E:\\record_files'
#判断下目录下方是否有这个文件夹
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    print('Directory', dir_name, 'created.')
else:
    print('Directory', dir_name, 'already exists.')
 
def main():
    while True:
        del_files()
        recode('SYNCED')
        print('有bug烦请联系ratangao 初版demo 欢迎试用提出问题.jpg')
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
    video = cv2.VideoWriter(f'{VIDEO_FILE_PATH}\\{file_name}.mp4v', fourcc, FPS, (width, height))
    # 7.记录开始录制视频的时间
    start_time = time.time()
    # 8.当录制时间不足1分钟时，循环写入到录像文件中
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
if __name__ == '__main__':
    main()
