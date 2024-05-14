import sys
import os
import subprocess
import re
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QTextEdit
import datetime




class ADBManager(QWidget):
    def __init__(self):
        super().__init__()
        self.adb_path = ('adb')  # ADB的路径
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.comboBox = QComboBox()
        layout.addWidget(self.comboBox)

        refreshButton = QPushButton('刷新设备列表')
        refreshButton.clicked.connect(self.refreshDevices)
        layout.addWidget(refreshButton)

        listPackagesButton = QPushButton('列出第三方包')
        listPackagesButton.clicked.connect(self.listPackages)
        layout.addWidget(listPackagesButton)

        adblogButton = QPushButton('导出ADBlog')
        adblogButton.clicked.connect(self.showadblogcat)
        layout.addWidget(adblogButton)

        installApkButton = QPushButton ('投屏')
        installApkButton.clicked.connect (self.Screenphone)
        layout.addWidget(installApkButton)

        displayButton = QPushButton ('截图')
        displayButton.clicked.connect (self.Screendisplay)
        layout.addWidget(displayButton)


        display2Button = QPushButton ('折叠屏/奇怪分辨率用这个')
        display2Button.clicked.connect (self.Screendisplay1)
        layout.addWidget(display2Button)


        self.logText= QTextEdit()
        self.logText.setReadOnly(True)
        layout.addWidget(self.logText)

        self.setLayout(layout)
        self.setWindowTitle('ADB装包器')
        self.refreshDevices()
        self.logText.append("<span style='color: black;'>runing~</span>")


    def refreshDevices(self):
        try:
            result = subprocess.run([self.adb_path, 'devices'], capture_output=True, text=True)
            devices = result.stdout.splitlines()
            device_list = [line.split('\t')[0] for line in devices[1:] if '\tdevice' in line]
            self.comboBox.clear()
            self.comboBox.addItems(device_list)
            self.logText.append("设备列表已刷新")
        except Exception as e:
            self.logText.append(f"刷新设备列表时发生错误: {str(e)}")



    def listPackages(self):
        try:
            current_device = self.comboBox.currentText()
            if not current_device:
                QMessageBox.warning(self, "警告", "没有选定的设备")
                return

            # 获取所有第三方包
            result = subprocess.run([self.adb_path, '-s', current_device, 'shell', 'pm', 'list', 'packages', '-3'],
                                    capture_output=True, text=True)
            if "error" in result.stderr.lower():
                self.logText.append("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
                QMessageBox.warning(self, "错误", "设备未授权或无法连接")
                return

            packages = result.stdout.split()
            formatted_packages = "<br>".join([f"<span style='color: blue;'>{package}</span>" for package in packages])
            self.logText.append(f"<b>第三方包列表:</b><br>{formatted_packages}")

            # 定义需要检查的包名及其描述
            package_names = {
                'com.camelgames.aoz.test': "Olinetest包",
                'com.camelgames.aoz.debuglz4': "Debug包",
                'com.camelgames.aoz.zhatest': "CnOlinetest包",
                'com.camelgames.aoz.zha': "CN包",
                'com.camelgames.aoz': "主包"
            }

            # 检查并显示特定包的versionCode信息
            for package_name, description in package_names.items():
                if any(package_name in package for package in packages):
                    commands = f'{self.adb_path} -s {current_device} shell dumpsys package {package_name}'
                    result = subprocess.run(commands, shell=True, capture_output=True, text=True)
                    version_code_match = re.search(r'versionCode=(\d+)', result.stdout)
                    if version_code_match:
                        version_code = int(version_code_match.group(1))
                        version_text = "37版本" if version_code > 2150 else "29版本"
                        self.logText.append(
                            f"<span style='color: green;'>{description}已安装, versionCode信息: {version_code} ({version_text})</span><br>")
                    else:
                        self.logText.append(
                            f"<span style='color: red;'>{description}未安装或无法获取versionCode信息</span>")
                else:
                    self.logText.append(f"<span style='color: red;'>{description}未安装</span>")

        except Exception as e:
            self.logText.append(f"<span style='color: red;'>列出第三方包时发生错误: {str(e)}</span>")


    def Screenphone(self):
        current_device = self.comboBox.currentText()
        if current_device:
            command = f"scrcpy -s {current_device} "
            subprocess.Popen(command, shell=True)

            self.logText.append("<span style='color: green;'>runing  <br />  可以直接向串流窗口拖入apk来安装apk</span>")
        else:
            self.logText.append("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning(self, "错误", "设备未授权或无法连接")
        return

    def showadblogcat(self):
        current_device = self.comboBox.currentText()
        if current_device:
            command = f"{self.adb_path} -s {current_device} shell logcat > logcat.log -d "
            result = subprocess.run (command, shell=True, capture_output=True, text=True)
            self.logText.append ("logcat 已导出")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
            return

    def Screendisplay(self):
        current_device = self.comboBox.currentText()
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if current_device:
            command = f'{self.adb_path} -s {current_device} exec-out "screencap -p && sleep2" -p > {str(nowtime)}{current_device}.jpeg'
            subprocess.Popen(command, shell=True)
            self.logText.append("<span style='color: green;'>截图放在同级目录下<br />截图速度取决于设备的物理分辨率</span>")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
        return


    def Screendisplay1(self):
        current_device = self.comboBox.currentText()
        Ntime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if current_device:
            command = f'{self.adb_path} -s {current_device} shell screencap /sdcard/{str(Ntime)}{current_device}.png'
            command2 = f'{self.adb_path} -s {current_device} pull sdcard/{str(Ntime)}{current_device}.png'
            subprocess.Popen(command,shell=True)
            time.sleep(2)
            subprocess.Popen(command2,shell=True)

            self.logText.append("<span style='color: green;'>这个截图会有点慢，在手机的存储目录scard/下也会有图片，请定时清理 <br /> 截图放在同级目录下<br />截图速度取决于设备的物理分辨率</span>")
        else:
            self.logText.append ("<span style='color: red;'>错误: 设备未授权或无法连接</span>")
            QMessageBox.warning (self, "错误", "设备未授权或无法连接")
        return



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ADBManager()
    ex.show()
    sys.exit(app.exec_())