#写一个qt界面,用来对选定的windows窗口做指定操作,且预留六个按钮用来执行对这个窗口的操作,再预留一个文本输出窗口,输出代码执行结果  
#1.选择窗口
#2.选择操作
#3.执行操作
#4.输出结果
#5.退出




import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('窗口操作')
        self.setGeometry(100, 100, 500, 300)

        #创建按钮
        self.btn1 = QPushButton('选择窗口', self)
        self.btn1.move(10, 10)
        self.btn1.clicked.connect(self.selectWindow)

        self.btn2 = QPushButton('选择操作', self)
        self.btn2.


