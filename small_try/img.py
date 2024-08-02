import os
from PIL import Image


def resize_images(directory, new_size):
    for filename in os.listdir (directory):
        if filename.endswith ((".jpg", ".jpeg", ".png", ".bmp")):
            file_path = os.path.join (directory, filename)
            with Image.open (file_path) as img:
                # 使用LANCZOS重采样方法进行高质量调整
                resized_img = img.resize (new_size, Image.LANCZOS)

                # 生成新的文件名，保留原始文件
                name, ext = os.path.splitext (filename)
                new_filename = f"{name}_resized{ext}"
                new_file_path = os.path.join (directory, new_filename)

                # 保存调整后的图片
                resized_img.save (new_file_path, quality=100)
                print (f"已调整 {filename} 的大小并保存为 {new_filename}")


# 使用示例
directory = "D:/wallpapers/deepnodezq-mas"  # 替换为您的图片目录路径
new_size = (512, 512)  # 设置新的像素大小，这里是宽800像素，高600像素

resize_images (directory, new_size)