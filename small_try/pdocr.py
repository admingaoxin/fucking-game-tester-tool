from paddleocr import PaddleOCR

def ocr_with_coordinates(image_path):
    # 初始化 PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 使用中文识别
    # 识别图片中的文字
    ocr_result = ocr.ocr(image_path, cls=True)

    # 存储识别结果和坐标
    results = []
    for line in ocr_result:
        for word_info in line:
            # 获取识别结果的文字信息和坐标
            text = word_info[1][0]
            coordinates = word_info[0]
            results.append((text, coordinates))

    return results

# 使用示例
image_path = 'now.png'
results = ocr_with_coordinates(image_path)
for text, coords in results:
    print(f"识别到的文字: {text}, 坐标: {coords}")