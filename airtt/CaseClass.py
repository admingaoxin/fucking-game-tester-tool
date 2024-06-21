from airtest.core.api import *
from jenkinsfile import startapp
condition = False
queren = (Template(r"确认.png"))

template = Template(r"tpl1606730579419.png", target_pos=5)

# 调用 touch 函数并捕获返回的坐标
clicked_position = touch(template)

# 打印点击的位置坐标
print("Clicked position:", clicked_position)

def Startapp():
    start_app(f"{startapp}")
    sleep(15)
    while True:
        if exists(queren):
            touch(queren)
        # elif exists(Template(r"tpl1718803009965.png", record_pos=(0.007, 0.508), resolution=(1080, 2312))):
        #     touch(Template(r"tpl1718803029180.png", record_pos=(-0.388, 0.856), resolution=(1080, 2312)))
        elif exists(Template(r"tpl1718803476859.png", record_pos=(0.422, 0.597), resolution=(1080, 2312))):
            break

        elif not condition and exists(Template (r"tpl1718803029180.png", record_pos=(-0.388, 0.856), resolution=(1080, 2312))):
            clicked_position = exists(Template (r"tpl1718803029180.png", record_pos=(-0.388, 0.856), resolution=(1080, 2312)))
            condition = True
        else :
            touch(clicked_position)

#  #返回坐标
# zuobiao = (Template(r"tpl1718863574528.png", record_pos=(-0.38, 0.853), resolution=(1080, 2312)))
# # touch(Template(r"tpl1718863574528.png", record_pos=(-0.38, 0.853), resolution=(1080, 2312)))
#
# exists(zuobiao)
# clicked_position = exists(zuobiao)
# print(clicked_position)
# touch(clicked_position)
#
# sleep(15)
#
# touch(clicked_position)
