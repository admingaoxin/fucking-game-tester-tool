from airtest.core.api import *
from config.jenkinsfile import startapp
from paddleocr import PaddleOCR
import time

workdir = f"C:\\Users\\cm619\\.jenkins\\workspace\\test\\cassclase\\ocr"


def Startapp():
    condition = False
    updatebultten = False
    queren = (Template (r"确认.png"))
    start_app (f"{startapp}")
    sleep(15)
    while True:
        if not updatebultten and exists (queren):
            touch (queren)
            updatebultten = True
        # elif exists(Template(r"tpl1718803009965.png", record_pos=(0.007, 0.508), resolution=(1080, 2312))):
        #     touch(Template(r"tpl1718803029180.png", record_pos=(-0.388, 0.856), resolution=(1080, 2312)))
        elif exists (Template (r"探索.png", record_pos=(0.422, 0.597), resolution=(1080, 2312))):
            break

        elif not condition and exists (
                Template (r"大地图切换.png", record_pos=(-0.388, 0.856), resolution=(1080, 2312))):
            clicked_position = exists (
                Template (r"大地图切换.png", record_pos=(-0.388, 0.856), resolution=(1080, 2312)))
            condition = True
        elif condition:
            touch (clicked_position)


@logwrap
def ocr_touch(target_text):
    nowtime = time.time ()
    ocr = PaddleOCR (use_angle_cls=True, lang='ch')
    # 截屏
    pic_path = f"{workdir}\\{nowtime}ocr.png"
    snapshot (pic_path)

    # 使用PaddleOCR识别文字
    ocr_result = ocr.ocr (pic_path, cls=True)
    # 遍历识别结果，找到目标文字的坐标
    target_coords = None
    for line in ocr_result:
        for word_info in line:
            # 获取识别结果的文字信息
            textinfo = word_info[1][0]
            print (textinfo)

            if target_text in textinfo:
                # 获取文字的坐标（中心点）
                x1, y1 = word_info[0][0]
                x2, y2 = word_info[0][2]
                target_coords = ((x1 + x2) / 2, (y1 + y2) / 2)
                break
        if target_coords:
            break

    # 点击坐标
    if target_coords:
        log ('success', '', '成功找到了')

        touch (target_coords)
    else:
        log ('error', '', '未找到目标文字')
        print (f"未找到目标文字：{target_text}", errors=1)


"""
#
# template = Template(r"tpl1606730579419.png", target_pos=5)
#
# # 调用 touch 函数并捕获返回的坐标
# clicked_position = touch(template)
#
# # 打印点击的位置坐标
# print("Clicked position:", clicked_position)

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
"""