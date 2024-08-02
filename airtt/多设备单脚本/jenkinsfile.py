import os

"""
参数化执行的手机
"""



devcath ={
    'ALL': 'ALL',
    'P30': 'JRQ4C19425001098',
    'K40': 'df92fc9b'
}
devpath = os.environ['deva']
for devpath1,devname in devcath.items():
    print(devpath1,devname)
    if devpath1 == devpath:
        dev = devname
        print(dev)
        break
    else:
        print('没有找到设备')



case_name ={
    'TRY': 'try.air',
    'TALK': 'talk.air',
    'talk1': '1.air',
    'test':'test.air'
}

casepath = os.environ['testcase']
for casepath1,casename in case_name.items():
    print(casepath1,casename)
    if casepath1 == casepath:
        air = casename
        print(air)
        break
    else:
        print('没有找到case')


"""
参数化执行的包体
"""

startapps ={
    'com.camelgames.aoz.test': "Olinetest",
    'com.camelgames.aoz.debuglz4': "debug",
    'com.camelgames.aoz.zhatest': "CnOlinetest",
    'com.camelgames.aoz.zha': "CN",
    'com.camelgames.aoz': "Google",
}
startapp = os.environ['testapp']
for startname,startapp1 in startapps.items():
    print(startname,startapp1)
    if startapp1 == startapp:
        startapp = startapp1
        print(startapp)
        break
    else:
        print('没有找到app')