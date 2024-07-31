import os
from PIL import Image

def resize_images(directory, new_size):
    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):
            file_path = os.path.join(directory, filename)
            with Image.open(file_path) as img:
                resized_img = img.resize(new_size)
                resized_img.save(file_path)
                print(f"已调整 {filename} 的大小")

# 使用示例
directory = "D:/wallpapers/deepnodezq-mas"  # 替换为您的图片目录路径
new_size = (512, 512)  # 设置新的像素大小，这里是宽800像素，高600像素

resize_images(directory, new_size)