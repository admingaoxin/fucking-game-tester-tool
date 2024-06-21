# import pandas as pd
# import os
# import sys
# import openpyxl
#
# file1 = "108-道具信息表.xlsm"
# file2 = "108-道具信息表1.xlsm"
#
# # diff_table = file1.compare(file2)
# #
# #
# # print(diff_table)
# def compare_excel(file1, file2):
#     # 读取两个Excel文件
#     df1 = pd.read_excel(file1)
#     df2 = pd.read_excel(file2)
#
#     # 比较两个DataFrame，找出不同之处
# diff_df = file1.compare(file2)
#
#     # 将结果输出到新的Excel文件
# diff_df.to_excel(os.path.join(\:try, 'excel_diff.xlsx'), index=False)
# #
# print("差异已保存到excel_diff.xlsx文件中。")
#
#
#
#




# import pandas as pd
# import openpyxl
# import difflib
#
# # file1 = "108-道具信息表.xlsm"
# # file2 = "108-道具信息表1.xlsm"
#
#
# file1 = "1.xlsx"
# file2 = "2.xlsx"
# def compare_excel(file1, file2):
#     # 读取两个Excel文件
#     df1 = pd.read_excel(file1)
#     df2 = pd.read_excel(file2)
#     # 示例用法
#
#     # compare_excel(file1, file2)
#     # print(compare_excel)
#     # 比较两个DataFrame，找出不同之处
#     diff_df = df1.compare(df2)
#
#     # 将结果输出到新的Excel文件
#     diff_df.to_excel("excel_diff.xlsx", index=False)
#
#     print("差异已保存到excel_diff.xlsx文件中。")


import pandas as pd
import difflib
import openpyxl
# 读取Excel文件
file1 = '108-道具信息表.xlsm'
file2 = '108-道具信息表1.xlsm'

# file1 = '108-道具信息表.xlsm"
# file2 = "108-道具信息表1.xlsm"
df1 = pd.read_excel(file1, engine='openpyxl')
df2 = pd.read_excel(file2, engine='openpyxl')
# 对比两个表格的差异
diff = difflib.unified_diff(str(df1).splitlines(), str(df2).splitlines())
diff_list = list(diff)
diff_str = ''.join(diff_list)
# 输出差异结果
print(diff_str)

d = difflib.HtmlDiff()
htmlContent = d.make_file(df1.to_string(),df2.to_string())

with open('diff.html','w') as f:
    f.write(htmlContent)


