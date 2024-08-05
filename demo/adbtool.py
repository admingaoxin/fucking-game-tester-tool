import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
import subprocess
import re
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QTextEdit, QLineEdit, QHBoxLayout, QLabel
import datetime
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIntValidator
from qt_material import apply_stylesheet
import asyncio
import aiohttp
import logging

logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s - %(message)s')

dir_name = 'log_files'
dir_name1 = 'screen_files'
dir_name2 = 'video_files'

class TabDemo(QTabWidget):
    def __init__(self, parent=None):
        super(TabDemo, self).__init__(parent)
        self.setWindowTitle ('胖虎の小工具')
        # 创建3个选项卡小控件窗口
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "ADB工具")
        self.addTab(self.tab2, "http协议请求")
        # self.addTab(self.tab3, "socketdemo")

        # 每个选项卡自定义的内容
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    def tab1UI(self):
        self.adb_manager = ADBManager()
        layout = QVBoxLayout()
        layout.addWidget(self.adb_manager)
        self.tab1.setLayout(layout)


    def tab2UI(self):
        self.http_manager = HTTPManager ()
        layout = QVBoxLayout ()
        layout.addWidget (self.http_manager)
        self.tab2.setLayout (layout)


    def tab3UI(self):
        # 自定义Tab 3的内容
        pass

class ADBManager(QWidget):
    def __init__(self):
        super().__init__()
        self.adb_path = 'adb'  # ADB的路径
        self.custom_variables = {"movetime": "从这里输入"}
        layout = QVBoxLayout ()
        self.comboBox = QComboBox ()
        self.comboBox1 = QComboBox ()
        layout.addWidget (self.comboBox)
        layout.addWidget (self.comboBox1)
        self.logText = QTextEdit ()
        # layout.addWidget(self.logText)

        self.number_boxes = {}
        for variable_name, label_name in self.custom_variables.items ():
            number_box = QLineEdit ()
            hbox = QHBoxLayout ()
            hbox.addWidget (QLabel (f"{label_name}："))
            hbox.addWidget (number_box)
            self.number_boxes[variable_name] = number_box
            layout.addLayout (hbox)

        refreshButton = QPushButton ('刷新设备列表')
        refreshButton.clicked.connect (self.refreshDevices)

        ADBshelltopButton = QPushButton ('根据输入刷新应用列表')
        ADBshelltopButton.clicked.connect (self.Listapp)

        listPackagesButton = QPushButton ('列出当前安装aoz包渠道和版本')
        listPackagesButton.clicked.connect (self.listPackages)

        adblogButton = QPushButton ('导出ADBlog')
        adblogButton.clicked.connect (self.showadblogcat)

        installApkButton = QPushButton ('投屏')
        installApkButton.clicked.connect (self.Screenphone)

        displayButton = QPushButton ('使用设备物理分辨率截图到本地')
        displayButton.clicked.connect (self.Screendisplay)

        display2Button = QPushButton ('折叠屏/奇怪分辨率截图')
        display2Button.clicked.connect (self.Screendisplay1)

        ADBStartappButton = QPushButton ('启动应用')
        ADBStartappButton.clicked.connect (self.Start_app)

        ADBstopappButton = QPushButton ('杀进程')
        ADBstopappButton.clicked.connect (self.stop_app)

        screenAVButton = QPushButton ('录屏')
        screenAVButton.clicked.connect (self.screendAV)

        datacathButton = QPushButton ('使用输入筛选versionname')
        datacathButton.clicked.connect (self.datacath)

        screenAV2Button = QPushButton ('使用输入的字符串命名录制的视频')
        screenAV2Button.clicked.connect (self.screendinput)

        buttonLayout1 = QVBoxLayout ()
        buttonLayout1.addWidget (refreshButton)
        buttonLayout1.addWidget (listPackagesButton)
        buttonLayout1.addWidget (adblogButton)
        buttonLayout1.addWidget (ADBStartappButton)
        buttonLayout1.addWidget (ADBstopappButton)
        buttonLayout1.addWidget (datacathButton)

        buttonLayout2 = QVBoxLayout ()
        buttonLayout2.addWidget (ADBshelltopButton)
        buttonLayout2.addWidget (installApkButton)
        buttonLayout2.addWidget (displayButton)
        buttonLayout2.addWidget (display2Button)
        buttonLayout2.addWidget (screenAV2Button)
        buttonLayout2.addWidget (screenAVButton)

        buttonsLayout = QHBoxLayout ()
        buttonsLayout.addLayout (buttonLayout1)
        buttonsLayout.addLayout (buttonLayout2)

        layout.addLayout (buttonsLayout)
        layout.addWidget (self.logText)

        self.setLayout (layout)


        self.refreshDevices ()
        self.refreshDevices()
        layout.addWidget (self.logText)
        self.logText.append("<span style='color: black;'>欢迎使用，有问题找胖虎~</br>需要打开Android设备的开发者选项以及允许usb调试（哄蒙也是Android.jpg）</span>")



    def screendAV(self):

        current_device = self.comboBox.currentText ()
        if not current_device:
            QMessageBox.warning (self, "警告", "没有选定的设备")
            return
        self.logText.append (
            f"<span style='color: red;'>出现投屏窗口后就证明可以录屏<br />做完想录制的操作后关闭这个新出现的投屏<br />视频就会保存在vedio_files目录下<span>")
        nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        command = f"scrcpy -s {current_device}  --record {dir_name2}/{nowtime}.mp4"
        subprocess.Popen (command, shell=True)

    def run(self):
        # 判断下目录下方是否有这个文件夹
        fileslist = [dir_name, dir_name1, dir_name2]
        for i in fileslist:
            if not os.path.exists (i):
                os.makedirs (i)
                self.logText.append (f"Directory  {i}   已创建")
            else:

                self.logText.append (f"Directory  {i}  已存在")

        # def installApk(self):
        #     try:
        #         current_device = self.comboBox.currentText()
        #         if current_device:
        #             apk_path, _ = QFileDialog.getOpenFileName(self, "选择APK文件", "", "APK files (*.apk)")
        #             if apk_path:
        #                 self.logText.append(f"开始安装APK: {apk_path}")
        #                 command = f"{self.adb_path} -s {current_device} install {apk_path}"
        #                 print(command)
        #                     # result = subprocess.Popen([self.adb_path, '-s', current_device, 'install', apk_path], capture_output=True, text=True)
        #                 result = subprocess.run(command, shell=True)
        #                 if "success" in result.stdout.lower():
        #                     self.logText.append("安装成功")
        #                     QMessageBox.information(self, "安装APK", "APK安装完成")
        #                 else:
        #                     self.logText.append(f"安装失败: {result.stderr}")
        #                     QMessageBox.warning(self, "安装APK", "安装失败，请检查设备是否授权和连接")
        #         else:
        #             QMessageBox.warning(self, "警告", "没有选定的设备")
        #     except Exception as e:
        #         self.logText.append(f"安装APK时发生错误: {str(e)}")


    def datacath(self):
        for name, number_box in self.number_boxes.items ():
            setattr (self, name, number_box.text ())  # float (number_box.text ())
        jiuer = self.movetime  #
        self.logText.append (f"获取到的输入是:{jiuer}")
        try:
            current_device = self.comboBox.currentText ()
            if not current_device:
                QMessageBox.warning (self, "警告", "没有选定的设备")
                return

            # 获取所有第三方包
            result = subprocess.run (
                [self.adb_path, '-s', current_device, 'shell', 'pm', 'list', 'packages', '-3' '|', 'grep', jiuer],
                capture_output=True, text=True)
            if "error" in result.stderr.lower ():
                self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
                QMessageBox.warning (self, "错误", "设备未授权或无法连接")
                return

            packages = result.stdout.split ()
            formatted_packages = "<br>".join ([f"<span style='color: blue;'>{package}</span>" for package in packages])
            self.logText.append (f"<b>筛选出的应用包:</b><br>{formatted_packages}")
            package_names = result.stdout.split ()
            package_list = [line.split ('\t')[0].replace ('package:', '') for line in packages[0:]]
            print (package_list)
            for package_name in package_list:
                print (package_name)
                # 检查并显示特定包的versionCode信息
                if package_name in package_list:
                    commands = f'{self.adb_path} -s {current_device} shell dumpsys package {package_name}'
                    result = subprocess.run (commands, shell=True, capture_output=True, text=True)
                    # version_code_match = re.search (r'versionCode=(\d+)', result.stdout)
                    versionName_code_match = re.search (r'versionName=(\d+.\d+.\d+.)', result.stdout)

                    if versionName_code_match:
                        # version_code = int (version_code_match.group (1))
                        version_name = versionName_code_match.group (1)
                        # version_text = "37版本" if version_code > 2150 else "29版本"
                        self.logText.append (
                            f"<span style='color: green;'> 筛选的包名：{package_name},versionName：{version_name}</span><br>")
                    else:
                        self.logText.append (
                            f"<span style='color: red;'>未安装或无法获取versionCode信息</span>")
                else:
                    self.logText.append (f"<span style='color: red;'>未安装</span>")

        except Exception as e:
            self.logText.append (f"<span style='color: red;'>列出第三方包时发生错误: {str (e)}</span>")

    def screendinput(self):
        for name, number_box in self.number_boxes.items ():
            setattr (self, name, number_box.text ())  # float (number_box.text ())
        jiuer = self.movetime
        current_device = self.comboBox.currentText ()
        if not current_device:
            QMessageBox.warning (self, "警告", "没有选定的设备")
            return
        self.logText.append (
            f"<span style='color: red;'>调试中，慎用<span>")
        nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        command = f"scrcpy -s {current_device}  --record {dir_name2}/{nowtime}{jiuer}.mp4"
        subprocess.Popen (command, shell=True)

    def refreshDevices(self):
        try:
            result = subprocess.run ([self.adb_path, 'devices'], capture_output=True, text=True)
            devices = result.stdout.splitlines ()
            device_list = [line.split ('\t')[0] for line in devices[1:] if '\tdevice' in line]
            self.comboBox.clear ()
            self.comboBox.addItems (device_list)
            self.logText.append ("设备列表已刷新")
        except Exception as e:
            self.logText.append (f"刷新设备列表时发生错误: {str (e)}")

    def Listapp(self):
        current_device = self.comboBox.currentText ()
        for name, number_box in self.number_boxes.items ():
            setattr (self, name, number_box.text ())  # float (number_box.text ())
        jiuer = self.movetime

        try:
            command = f"{self.adb_path} -s {current_device} shell pm list packages -3 |grep {jiuer}"
            result = subprocess.run (command, capture_output=True, text=True)
            apps = result.stdout.splitlines ()
            app_list = [line.split ('\t')[0].replace ('package:', '') for line in apps[0:]]  # if '\tpackage:' in line
            self.comboBox1.clear ()
            self.comboBox1.addItems (app_list)
            self.logText.append ("应用列表已刷新")
        except Exception as e:
            self.logText.append (f"刷新应用列表时发生错误: {str (e)}")

    def Start_app(self):
        current_device = self.comboBox.currentText ()
        current_applist = self.comboBox1.currentText ()
        command = f"{self.adb_path} -s {current_device} shell monkey -p {current_applist} -c android.intent.category.LAUNCHER 1 "
        result = subprocess.Popen (command, shell=True)

    def stop_app(self):
        current_device = self.comboBox.currentText ()
        current_applist = self.comboBox1.currentText ()
        command = f"{self.adb_path} -s {current_device} shell am force-stop {current_applist} "
        result = subprocess.Popen (command, shell=True)

    def Wifi_devices(self):
        current_device = self.comboBox.currentText ()
        command = f"{self.adb_path} -s {current_device} shell   ifconfig wlan0 "
        command1 = f"{self.adb_path} connect device_ip_address"
        result = subprocess.Popen (command, text=True)

    def listPackages(self):
        try:
            current_device = self.comboBox.currentText ()
            if not current_device:
                QMessageBox.warning (self, "警告", "没有选定的设备")
                return

            # 获取所有第三方包
            result = subprocess.run ([self.adb_path, '-s', current_device, 'shell', 'pm', 'list', 'packages', '-3'],
                                     capture_output=True, text=True)
            if "error" in result.stderr.lower ():
                self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
                QMessageBox.warning (self, "错误", "设备未授权或无法连接")
                return

            packages = result.stdout.split ()
            formatted_packages = "<br>".join ([f"<span style='color: blue;'>{package}</span>" for package in packages])
            # self.logText.append (f"<b>第三方包列表:</b><br>{formatted_packages}")

            # 定义需要检查的包名及其描述
            package_names = {
                'com.camelgames.aoz.test': "Olinetest包",
                'com.camelgames.aoz.debuglz4': "Debug包",
                'com.camelgames.aoz.zhatest': "CnOlinetest包",
                'com.camelgames.aoz.zha': "CN包",
                'com.camelgames.aoz': "主包",
                'com.camelgames.aoz.huawei': "华为包",
                'yunbao.aoz.tt': "抖音本地包",
                'com.yungame.aoz.tt': "抖音云包"
            }

            # 检查并显示特定包的versionCode信息
            for package_name, description in package_names.items ():
                if any (package_name in package for package in packages):
                    commands = f'{self.adb_path} -s {current_device} shell dumpsys package {package_name}'
                    result = subprocess.run (commands, shell=True, capture_output=True, text=True)
                    version_code_match = re.search (r'versionCode=(\d+)', result.stdout)
                    versionName_code_match = re.search (r'versionName=(\d+.\d+.\d+.)', result.stdout)
                    if version_code_match:
                        version_code = int (version_code_match.group (1))
                        version_name = versionName_code_match.group (1)
                        version_text = "37版本" if version_code > 2150 else "29版本"
                        self.logText.append (
                            f"<span style='color: green;'>{description}已安装, versionCode信息: {version_code} ({version_text}),versionName：{version_name}</span><br>")
                    else:
                        self.logText.append (
                            f"<span style='color: red;'>{description}未安装或无法获取versionCode信息</span>")
                else:
                    self.logText.append (f"<span style='color: red;'>{description}未安装</span>")

        except Exception as e:
            self.logText.append (f"<span style='color: red;'>列出第三方包时发生错误: {str (e)}</span>")

    def Screenphone(self):
        current_device = self.comboBox.currentText ()
        if current_device:
            command = f"scrcpy -s {current_device} "
            process = subprocess.Popen (command, shell=True, text=True)
            # stdout, stderr = process.communicate ()
            # logging.info(f"{stdout}")
            # logging.info(f"{stderr}")

            self.logText.append (
                "<span style='color: green;'>runing  <br />  可以直接向串流窗口拖入apk来安装apk</span>")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
        return

    def showadblogcat(self):
        current_device = self.comboBox.currentText ()
        nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        if current_device:
            command = f"{self.adb_path} -s {current_device} shell logcat > {dir_name}/{str (nowtime)}{current_device}logcat.log -d "
            subprocess.Popen (command, shell=True)
            self.logText.append ("logcat 已导出")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
            return

    def Screendisplay(self):
        current_device = self.comboBox.currentText ()
        nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        if current_device:
            command = f'{self.adb_path} -s {current_device} exec-out "screencap -p && sleep2" -p > {dir_name1}/{str (nowtime)}{current_device}.png'
            subprocess.Popen (command, shell=True)
            self.logText.append (
                "<span style='color: green;'>截图放在screen_files下<br />截图速度取决于设备的物理分辨率</span>")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
        return

    def Screendisplay1(self):
        current_device = self.comboBox.currentText ()
        Ntime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        if current_device:
            self.logText.append (
                "<span style='color: green;'>这个截图会有点慢，在手机的存储目录scard/下也会有图片，请定时清理 <br /> 截图放在screen_files下<br />截图速度取决于设备的物理分辨率</span>")
            command = f'{self.adb_path} -s {current_device} shell screencap /sdcard/{str (Ntime)}{current_device}.png'
            command2 = f'{self.adb_path} -s {current_device} pull sdcard/{str (Ntime)}{current_device}.png {dir_name1}/{str (Ntime)}{current_device}.png'
            subprocess.Popen (command, shell=True)
            time.sleep (3)
            subprocess.Popen (command2, shell=True)
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
        return

    def pulllog(self):
        current_device = self.comboBox.currentText ()
        current_applist = self.comboBox1.currentText ()
        try:
            current_device and current_applist
            command = f'{self.adb_path} -s {current_device} pull sdcard/Android/data/{current_applist}/files/_LOG.log'
            subprocess.Popen (command, shell=True)
        except Exception as e:
            self.logText.append (f"请选择要导出log的aoz包体: {str (e)}")
            self.logText.append ("<span style='color: red;'>请选择要导出log的aoz包体</span>")

    def ADBshelltop(self):
        current_device = self.comboBox.currentText ()
        if current_device:
            command = f'{self.adb_path} -s {current_device} shell top'
            subprocess.Popen (command)
            self.logText.append (
                "<span style='color: red;'>会一直打印基础占用<br />不要在powershell窗口ctrl+c<br /> 下面是参数详解：</span>")
            self.logText.append ("<span style='color: green;'>PID — 进程id <br /> USER — 进程所有者  <br />PR — 进程优先级  <br "
                                 "/>NI — nice值。负值表示高优先级，正值表示低优先级 <br /> VIRT — 进程使用的虚拟内存总量，单位kb。VIRT = SWAP + RES <br "
                                 "/>  RES — 进程使用的、未被换出的物理内存大小，单位kb。RES = CODE + DATA <br />  SHR — 共享内存大小，单位kb <br /> "
                                 "S — 进程状态。D = 不可中断的睡眠状态 R = 运行S = 睡眠 T = 跟踪 / 停止 Z = 僵尸进程 <br />  %CPU — "
                                 "上次更新到现在的CPU时间占用百分比 <br />   %MEM — 进程使用的物理内存百分比<br /> TIME + — 进程使用的CPU时间总计，单位1 / "
                                 "100秒  <br /> COMMAND — 进程名称（命令名 / 命令行） </span>")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
        return

class HTTPManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('请求地址')

        self.method_combo = QComboBox(self)
        self.method_combo.addItem('GET')
        self.method_combo.addItem('POST')

        self.send_count_input = QLineEdit(self)
        self.send_count_input.setPlaceholderText('请求次数（必须是整数int）')
        self.send_count_input.setValidator(QIntValidator())

        self.body_input = QTextEdit(self)
        self.body_input.setPlaceholderText('请输入请求体（默认请求头写死是application/json）')

        self.send_btn = QPushButton('Send', self)
        self.send_btn.clicked.connect(self.send_request)

        self.logText = QTextEdit()
        self.logText.setReadOnly(True)

        layout.addWidget(self.url_input)
        layout.addWidget(self.method_combo)
        layout.addWidget(self.body_input)
        layout.addWidget(self.send_count_input)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.logText)  # 添加日志文本框到布局

        self.setLayout(layout)


    @pyqtSlot ()  # 标记为Qt槽，确保在GUI线程中调用
    def send_request(self):
        url = self.url_input.text ()
        method = self.method_combo.currentText ()
        send_count = int (self.send_count_input.text ()) if self.send_count_input.text () else 1
        asyncio.run (self.send_requests_async (url, method, send_count))
        self.logText.append (f"请求已发送，在同级文件夹下的log中查看返回")

    async def send_requests_async(self, url, method, send_count):
        body = self.body_input.toPlainText ().encode ('utf-8') if method == 'POST' else None

        tasks = []
        if method == 'GET':
            tasks = [self.send_get_request_async (url) for _ in range (send_count)]
        elif method == 'POST':
            tasks = [self.send_post_request_async (url, body) for _ in range (send_count)]

        await asyncio.gather (*tasks)

    async def send_get_request_async(self, url):
        try:
            async with aiohttp.ClientSession () as session:
                async with session.get (url) as response:
                    text = await response.text ()
                    # 记录日志而不是更新GUI
                    logging.info (f"GET {url} Status Code: {response.status}")
                    logging.info (f"Response: {text[:10000]}...")
        except Exception as e:
            logging.error (f"GET {url} Error: {e}")

    async def send_post_request_async(self, url, body):
        headers = {'Content-Type': 'application/json'}
        try:
            async with aiohttp.ClientSession () as session:
                async with session.post (url, data=body, headers=headers) as response:
                    text = await response.text ()
                    # 在这里你可以决定如何处理响应，例如记录日志或更新GUI
                    logging.info (f"POST {url} Status Code: {response.status}")
                    logging.info (f"Response: {text[:10000]}...")
        except Exception as e:
            logging.error (f"POST {url} Error: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet (app, theme='light_blue_500.xml')
    demo = TabDemo()
    demo.show()
    sys.exit(app.exec_())