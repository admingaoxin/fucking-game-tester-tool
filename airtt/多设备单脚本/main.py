_author_ = "AirtestProject"

from airtest.core.api import *
from airtest.core.android.android import *
import time
from airtest.core.android.adb import *
"""
# 什么都不填写，默认取当前连接中的第一台手机
Android:///
# 连接本机默认端口连的一台设备号为79d03fa的手机
Android://127.0.0.1:5037/79d03fa
# 用本机的adb连接一台adb connect过的远程设备，注意10.254.60.1:5555其实是serialno
Android://127.0.0.1:5037/10.254.60.1:5555
"""
connect_device("Android:///")  #同样是设备字符串
print(connect_device)
print(device())
auto_setup(devices=["Android:///"], compress=90)

android = Android()
print("***************")
print(android.get_default_device())
print(auto_setup())
Olinetest = 'com.camelgames.aoz.test'
Debug = 'com.camelgames.aoz.debuglz4'
devices = str(android.get_default_device())
print(devices)

p30 = 'JRQ4C19425001098'

if p30  in devices:
    print('在测试机型是p30')
    android.list_app(third_only=True)
    print(android.list_app(third_only=True))
    android.get_top_activity()
    print(android.get_top_activity())
    if Debug in android.get_top_activity():
        print('is runing')

        auto_setup(__file__, logdir=True)
    else:
        start_app(Debug)
        auto_setup (__file__, logdir=True)

time.sleep(2)



    # package_names = {
    #     'com.camelgames.aoz.test': "Olinetest包",
    #     'com.camelgames.aoz.debuglz4': "Debug包",
    #     'com.camelgames.aoz.zhatest': "CnOlinetest包",
    #     'com.camelgames.aoz.zha': "CN包",
    #     'com.camelgames.aoz': "主包"