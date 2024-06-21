import os
import pytesseract
from PIL import Image

# 设置tesseract的安装路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 定义一个函数，用于识别图片中的文字并保存到txt文件中
def ocr_image(image_path, output_path):
    # 打开图片文件
    image = Image.open(image_path)

    # 使用pytesseract识别图片中的文字
    text = pytesseract.image_to_string(image, lang='chi_sim')

    # 将识别出的文字保存到txt文件中
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

# 定义一个函数，用于遍历文件夹中的所有图片文件，并调用ocr_image函数进行识别和保存
def ocr_folder(folder_path, output_folder):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 判断文件是否为图片文件
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # 构造图片文件的完整路径和txt文件的完整路径
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename.replace('.jpg', '.txt').replace('.png', '.txt'))

            # 调用ocr_image函数进行识别和保存
            ocr_image(image_path, output_path)

# 调用ocr_folder函数进行识别和保存
ocr_folder('image_folder', 'output_folder')