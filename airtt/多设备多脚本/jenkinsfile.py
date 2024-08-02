import os

# 参数化执行的手机
devcath = {
    'ALL': 'ALL',
    'P30': 'JRQ4C19425001098',
    'K40': 'df92fc9b'
}
devpath = os.environ['deva']
for devpath1, devname in devcath.items():
    if devpath1 == devpath:
        dev = devname
        break
else:
    raise ValueError('没有找到设备')

# 参数化执行的case
case_name = {
    'TRY': 'try.air',
    'TALK': 'talk.air',
    'talk1': '1.air',
    'test': 'test.air'
}
casepaths = os.environ['testcase'].split(',')
airs = []
print(casepaths)
for casepath in casepaths:
    casepath = casepath.strip()  # 去除前后空格
    if casepath in case_name:
        airs.append(case_name[casepath])
if not airs:
    raise ValueError('没有找到case')


# 参数化执行的包体
startapps = {
    'com.camelgames.aoz.test': "Olinetest",
    'com.camelgames.aoz.debuglz4': "debug",
    'com.camelgames.aoz.zhatest': "CnOlinetest",
    'com.camelgames.aoz.zha': "CN",
    'com.camelgames.aoz': "Google",
}
startapp = os.environ['testapp']
for startname, startapp1 in startapps.items():
    if startapp1 == startapp:
        startapp = startapp1
        break
else:
    raise ValueError('没有找到app')