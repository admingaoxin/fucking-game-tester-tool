# -*- encoding=utf8 -*-
__author__ = "cm619"
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from airtest.core.api import *
auto_setup(__file__)

# from airtest.core.api import touch,wait

# from objecket import touch,wait



start_app("com.camelgames.aoz.debuglz4")
#一些图
yindao = (Template(r"tpl1716461390125.png", record_pos=(0.351, -0.259), resolution=(1080, 2312)))
juqing = (Template(r"tpl1716452021292.png", record_pos=(0.393, -0.915), resolution=(1080, 2312)))
AR=Template(r"tpl1716453334261.png")#, record_pos=(-0.306, -0.353), resolution=(1080, 2312)
BOOM = Template(r"tpl1716453349683.png")#, record_pos=(-0.297, -0.028), resolution=(1080, 2312)
WURENJI = Template(r"tpl1716453355580.png")#, record_pos=(-0.301, 0.314), resolution=(1080, 2312)
gecao = (AR,BOOM,WURENJI)

# start_recording(bit_rate_level=1)


wake()
# sleep(75)
wait(Template(r"22333.png"))
swipe(Template(r"tpl1716799701637.png", record_pos=(0.048, 0.731), resolution=(1080, 2312)), vector=[0.3816, -0.2615],duration=2)
#
#
wait(Template(r"tpl1716799755564.png", record_pos=(0.062, -0.404), resolution=(1080, 2312)))

swipe(Template(r"tpl1716799701637.png", record_pos=(0.048, 0.731), resolution=(1080, 2312)), vector=[0.0802, -0.4266],duration=1)

wait(Template(r"tpl1716451260833.png", record_pos=(0.033, -0.027), resolution=(1080, 2312)))

touch(Template(r"tpl1716451273092.png", record_pos=(0.014, 0.142), resolution=(1080, 2312)))
sleep(2)
touch(Template(r"tpl1716451301866.png", record_pos=(0.008, 0.447), resolution=(1080, 2312)))
sleep(30)
wait(Template(r"tpl1716800255711.png", record_pos=(0.002, 0.115), resolution=(1080, 2312)))
touch(Template(r"tpl1716800255711.png", record_pos=(0.002, 0.115), resolution=(1080, 2312)))
sleep(15)

count = 0
while True:



    if exists(yindao):
        touch(yindao)
    elif exists(juqing):
        touch(juqing)
        pass
    elif exists(Template(r"tpl1716817126979.png", record_pos=(0.132, -0.105), resolution=(1080, 2312))) or count >= 50:
        break

    else:
        found = False
        for template in gecao:
                if exists(template):
                    touch(template)
                    sleep(0.5)
                    touch(Template(r"tpl1716455540208.png", record_pos=(0.009, 0.613), resolution=(1080, 2312)))
                    found = True
                    break
    sleep(0.5)
    count += 1
print('轮询了'+str(count)+'次')
# # dev.stop_recording(output="test.mp4")

exists(Template(r"tpl1716817126979.png", record_pos=(0.132, -0.105), resolution=(1080, 2312)))
touch(Template(r"末日引导黑板手.png", record_pos=(0.132, -0.105), resolution=(1080, 2312)))

assert_exists(yindao)
touch(yindao)
assert_exists(yindao)
touch(yindao)

