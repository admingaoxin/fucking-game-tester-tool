import os

"""
参数化执行的手机
"""

devpath = os.environ['deva']
if devpath == 'ALL':
    dev = 'ALL'
elif devpath == 'P30':
    dev = 'JRQ4C19425001098'
elif devpath == 'K40':
    dev = 'df92fc9b'


"""
暂时先这么写，后面考虑用字典实现
"""

casepath = os.environ['testcase']
if casepath is None:
    air = None
elif casepath == 'TRY':
    air = 'try.air'
elif casepath == 'TALK':
    air = 'talk.air'


"""
参数化执行的包体
"""
startapp = os.environ['testapp']
if startapp == ' ':
    startapp = ''
elif startapp == 'debug':
    startapp = 'com.camelgames.aoz.debuglz4'


