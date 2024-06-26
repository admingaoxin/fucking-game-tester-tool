import sys
import os
import subprocess
import re
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QTextEdit,QLineEdit,QHBoxLayout,QLabel
import datetime
from qt_material import apply_stylesheet
import __future__

class ADBManager (QWidget):
    def __init__(self):
        super ().__init__ ()
        self.adb_path = ('adb')  # ADB的路径
        self.custom_variables = {"movetime" : "预留输入口"}
        self.initUI ()

    def initUI(self):
        layout = QVBoxLayout ()
        self.comboBox = QComboBox ()
        self.comboBox1 = QComboBox ()
        layout.addWidget (self.comboBox)
        layout.addWidget (self.comboBox1)

        self.number_boxes = {}
        for variable_name, label_name in self.custom_variables.items():
            number_box = QLineEdit()

            hbox = QHBoxLayout ()
            hbox.addWidget (QLabel (f"{label_name}："))
            hbox.addWidget (number_box)

            layout.addLayout (hbox)
            self.number_boxes[variable_name] = number_box

        refreshButton = QPushButton ('刷新设备列表')
        refreshButton.clicked.connect (self.refreshDevices)
        layout.addWidget (refreshButton)

        ADBshelltopButton = QPushButton ('刷新应用列表(只能选择aoz的包体)')
        ADBshelltopButton.clicked.connect (self.Listapp)
        layout.addWidget (ADBshelltopButton)

        listPackagesButton = QPushButton ('列出当前安装的渠道包和版本')
        listPackagesButton.clicked.connect (self.listPackages)
        layout.addWidget (listPackagesButton)

        adblogButton = QPushButton ('导出ADBlog')
        adblogButton.clicked.connect (self.showadblogcat)
        layout.addWidget (adblogButton)

        installApkButton = QPushButton ('投屏')
        installApkButton.clicked.connect (self.Screenphone)
        layout.addWidget (installApkButton)

        displayButton = QPushButton ('使用设备物理分辨率截图到本地')
        displayButton.clicked.connect (self.Screendisplay)
        layout.addWidget (displayButton)

        display2Button = QPushButton ('折叠屏/奇怪分辨率截图')
        display2Button.clicked.connect (self.Screendisplay1)
        layout.addWidget (display2Button)

        ADBStartappButton = QPushButton ('启动应用')
        ADBStartappButton.clicked.connect (self.Start_app)
        layout.addWidget (ADBStartappButton)

        ADBstopappButton = QPushButton ('杀进程')
        ADBstopappButton.clicked.connect (self.stop_app)
        layout.addWidget (ADBstopappButton)

        # ADBWifidevicesButton = QPushButton ('wifi')
        # ADBWifidevicesButton.clicked.connect (self.Wifi_devices)
        # layout.addWidget (ADBWifidevicesButton)

        # ADBStartappButton = QPushButton ('log提取')
        # ADBStartappButton.clicked.connect (self.pulllog)
        # layout.addWidget (ADBStartappButton)


        # ADBshelltopButton = QPushButton ('shell top')
        # ADBshelltopButton.clicked.connect(self.ADBshelltop)
        # layout.addWidget (ADBshelltopButton)

        ADBstopappButton = QPushButton ('录屏')
        ADBstopappButton.clicked.connect (self.linshi)
        layout.addWidget (ADBstopappButton)

        self.logText = QTextEdit ()
        self.logText.setReadOnly (True)
        layout.addWidget (self.logText)

        self.setLayout (layout)
        self.setWindowTitle ('胖虎の小工具')
        self.refreshDevices ()
        self.Listapp()
        # self.logText.append ("<span style='color: black;'>runing~</span>")


    def linshi(self):
        self.logText.append(f"<span style='color: red;'>出现投屏窗口后就证明可以录屏<br />做完想录制的操作后关闭这个新出现的投屏<br />视频就会保存在此目录下<span>")
        current_device = self.comboBox.currentText ()
        nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        # for name, number_box in self.number_boxes.items ():
        #     setattr(self, name, float (number_box.text ()))
        # jiuer =self.movetime    #
        """
        预留的，获取输入用的
        """
        command = f"scrcpy -s {current_device}  --record {nowtime}.mkv"
        subprocess.Popen(command,shell=True)

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
        try:
            command = f"{self.adb_path} -s {current_device} shell pm list packages -3 |grep .aoz"
            result = subprocess.run (command, capture_output=True, text=True)
            apps = result.stdout.splitlines ()
            app_list = [line.split('\t')[0].replace('package:', '') for line in apps[0:] ] #if '\tpackage:' in line
            self.comboBox1.clear ()
            self.comboBox1.addItems(app_list)
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
        result = subprocess.Popen (command,shell=True)


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
                'yunbao.aoz.tt' :"抖音本地包"
            }

            # 检查并显示特定包的versionCode信息
            for package_name, description in package_names.items ():
                if any(package_name in package for package in packages):
                    commands = f'{self.adb_path} -s {current_device} shell dumpsys package {package_name}'
                    result = subprocess.run (commands, shell=True, capture_output=True, text=True)
                    version_code_match = re.search (r'versionCode=(\d+)', result.stdout)
                    versionName_code_match= re.search(r'versionName=(\d+.\d+.\d+.)', result.stdout)
                    if version_code_match:
                        version_code = int (version_code_match.group (1))
                        version_name = versionName_code_match.group (1)
                        version_text = "37版本" if version_code > 2150 else "29版本"
                        self.logText.append (
                            f"<span style='color: green;'>{description}已安装, versionCode信息: {version_code} ({version_text}),版本：{version_name}</span><br>")
                    else:
                        self.logText.append (
                            f"<span style='color: red;'>{description}未安装或无法获取versionCode信息</span>")
                else:
                    self.logText.append(f"<span style='color: red;'>{description}未安装</span>")

        except Exception as e:
            self.logText.append (f"<span style='color: red;'>列出第三方包时发生错误: {str (e)}</span>")

    def Screenphone(self):
        current_device = self.comboBox.currentText ()
        if current_device:
            command = f"scrcpy -s {current_device} "
            subprocess.Popen (command, shell=True, text=True)

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
            command = f"{self.adb_path} -s {current_device} shell logcat > {str (nowtime)}{current_device}logcat.log -d "
            subprocess.Popen(command,shell=True)
            self.logText.append ("logcat 已导出")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
            return

    def Screendisplay(self):
        current_device = self.comboBox.currentText ()
        nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        if current_device:
            command = f'{self.adb_path} -s {current_device} exec-out "screencap -p && sleep2" -p > {str (nowtime)}{current_device}.png'
            subprocess.Popen (command, shell=True)
            self.logText.append (
                "<span style='color: green;'>截图放在同级目录下<br />截图速度取决于设备的物理分辨率</span>")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
        return

    def Screendisplay1(self):
        current_device = self.comboBox.currentText ()
        Ntime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
        if current_device:
            self.logText.append (
                "<span style='color: green;'>这个截图会有点慢，在手机的存储目录scard/下也会有图片，请定时清理 <br /> 截图放在同级目录下<br />截图速度取决于设备的物理分辨率</span>")
            command = f'{self.adb_path} -s {current_device} shell screencap /sdcard/{str (Ntime)}{current_device}.png'
            command2 = f'{self.adb_path} -s {current_device} pull sdcard/{str (Ntime)}{current_device}.png'
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
            subprocess.Popen(command,shell=True)
        except Exception as e:
            self.logText.append (f"请选择要导出log的aoz包体: {str (e)}")
            self.logText.append("<span style='color: red;'>请选择要导出log的aoz包体</span>")

    def ADBshelltop(self):
        current_device = self.comboBox.currentText ()
        if current_device:
            command = f'{self.adb_path} -s {current_device} shell top'
            subprocess.Popen(command)
            self.logText.append("<span style='color: red;'>会一直打印基础占用<br />不要在powershell窗口ctrl+c<br /> 下面是参数详解：</span>")
            self.logText.append("<span style='color: green;'>PID — 进程id <br /> USER — 进程所有者  <br />PR — 进程优先级  <br "
                                "/>NI — nice值。负值表示高优先级，正值表示低优先级 <br /> VIRT — 进程使用的虚拟内存总量，单位kb。VIRT = SWAP + RES <br "
                                "/>  RES — 进程使用的、未被换出的物理内存大小，单位kb。RES = CODE + DATA <br />  SHR — 共享内存大小，单位kb <br /> "
                                "S — 进程状态。D = 不可中断的睡眠状态 R = 运行S = 睡眠 T = 跟踪 / 停止 Z = 僵尸进程 <br />  %CPU — "
                                "上次更新到现在的CPU时间占用百分比 <br />   %MEM — 进程使用的物理内存百分比<br /> TIME + — 进程使用的CPU时间总计，单位1 / "
                                "100秒  <br /> COMMAND — 进程名称（命令名 / 命令行） </span>")
        else:
            self.logText.append("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning(self, "错误", "设备未授权或无法连接")
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet (app, theme='light_blue_500.xml')
    ex = ADBManager()
    ex.show()
    sys.exit(app.exec_())
