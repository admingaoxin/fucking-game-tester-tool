import pydirectinput
import pydirectinput
import time
import numpy
import cv2
import os
from skimage.metrics import structural_similarity as ssim
from constants import c_constants

c_constants = {
    'hold': 0.8, 
    # ...
}
holdK = 1.0
if c_constants['hold']:
    holdK = curWepone.hold * c_constants['hold']
#对比图片获取名字
def compareAndGetName(screenImg, dir):
    #获取目录下所有文件
    content = os.listdir(dir)
    name = 'none'
    max = 0
    #遍历文件
    for fileName in content:
        #使用opencv读取文件
        curWepone = cv2.imread(dir + fileName, 0)
        #使用SSIM算法拿到图片相似度
        res = calculate_ssim(numpy.asarray(screenImg), numpy.asarray(curWepone))
        #获取相似度最大的
        if max < res and res > 0.5:
            max = res
            name = str(fileName)[:-4]
    return name

def canFire():
    pydirectinput.move(xOffset=0, yOffset=10, relative=True)

def getCurrentWepone():
    # Your implementation here
    pass

def moveMouse(): 
    curWepone = getCurrentWepone()
    if (curWepone.name == 'none'):
        return
def calculate_ssim(img1, img2):
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return numpy.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(numpy.squeeze(img1), numpy.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')

def moveMouse(): 
    #从识别的数据中，再更具当前选择的武器，获取此刻的武器（比如按下1键，武器装备栏1为m762，那么此时武器就是m762）
    curWepone = getCurrentWepone()
    if (curWepone.name == 'none'):
        return
    #基础y轴补偿（没任何配件）
    basic = curWepone.basic
    #射速
    speed = curWepone.speed
    startTime = round(time.perf_counter(), 3) * 1000
    for i in range(curWepone.maxBullets):
        #是否可以开火，比如左键抬起，就中断。
        if not canFire():
            break
        #系数，比如开镜，就需要再原来基础上乘1.33
        holdK = 1.0
        if c_contants.hold:
            holdK = curWepone.hold
        #乘以系数后实际的移动距离
        moveSum = int(round(basic[i] * curWepone.k * holdK, 2))
        while True:
            if (moveSum > 10):
                #移动鼠标
                pydirectinput.move(xOffset=0, yOffset=10, relative=True)
                moveSum -= 10
            elif (moveSum > 0):
                pydirectinput.move(xOffset=0, yOffset=moveSum, relative=True)
                moveSum = 0
            elapsed = (round(time.perf_counter(), 3) * 1000 - startTime)
            if not canFire() or elapsed > (i + 1) * speed + 10:
                break
            time.sleep(0.01)

