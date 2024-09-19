from paddleocr import PaddleOCR, draw_ocr
import os
from PIL import Image
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=False) 
img_path = 'iamge\\2.png'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# 显示结果

result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores)
im_show = Image.fromarray(im_show)
save_folder = 'iamge\\'

# 检查文件夹是否存在，如果不存在则创建
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
im_show.save(os.path.join(save_folder, '01.jpg'))