import os
import pandas as pd

# 指定目录
directory = 'E:/nextqa/Ark/用例执行/S0全量测试/第一轮全量/功能测试/3C/芯片/属性/临时伤害属性检查用例'

# 获取目录及其子目录下所有Excel文件的路径
excel_files = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.xlsx'):
            excel_files.append(os.path.join(root, file))

# 读取Excel文件中的所有数据
data_frames = [pd.read_excel(file) for file in excel_files]

# 合并所有数据
merged_data = pd.concat(data_frames)

# 筛选出包含 "fail" 或 "block" 的行
filtered_data = merged_data[merged_data['测试结果'].isin(['Fail', 'Block','当前版本不生效'])]

# 将筛选后的数据保存到一个新的Excel文件中
filtered_data.to_excel(os.path.join(directory, 'filtered_data.xlsx'), index=False)
