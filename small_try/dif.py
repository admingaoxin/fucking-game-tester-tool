import pandas as pd

def compare_tables_to_html(file1, file2, output_file):
    df1 = pd.read_excel(file1, engine='openpyxl')
    df2 = pd.read_excel(file2, engine='openpyxl')
    print(df1)

    compared_data = []
    max_rows = max(len(df1.index), len(df2.index))
    max_cols = max(len(df1.columns), len(df2.columns))

    for i in range(max_rows):
        row_data = []
        for j in range(max_cols):
            if i < df1.shape[0] and j < df1.shape[1] and i < df2.shape[0] and j < df2.shape[1]:
                if df1.iloc[i, j] == df2.iloc[i, j]:
                    row_data.append(df1.iloc[i, j])
                else:
                    row_data.append(
                        f"<span style='color:green'>{df1.iloc[i, j]}</span> → <span style='color:red'>{df2.iloc[i, j]}</span>")
            elif i < df1.shape[0] and j < df1.shape[1]:
                row_data.append(f"<span style='color:green'>{df1.iloc[i, j]}</span>")
            elif i < df2.shape[0] and j < df2.shape[1]:
                row_data.append(f"<span style='color:red'>{df2.iloc[i, j]}</span>")
            else:
                row_data.append('')
        compared_data.append(row_data)

    compared_df = pd.DataFrame(compared_data, columns=range(max_cols))

    # 生成HTML表格
    html_content = compared_df.to_html(classes='styled', escape=False, header=False, index=False, na_rep='')

    # 将HTML内容写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    compare_tables_to_html('2.xlsm', '1.xlsm', 'diff.html')