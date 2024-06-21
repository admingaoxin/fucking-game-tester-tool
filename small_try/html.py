import pandas as pd
from jinja2 import Template

def compare_tables_to_html(file1, file2, output_file):
    df1 = pd.read_excel(file1, engine='openpyxl')
    df2 = pd.read_excel(file2, engine='openpyxl')

    # 添加 '_file' 列标识文件来源
    df1['_file'] = 'file1'
    df2['_file'] = 'file2'

    # 合并两个DataFrame
    merged_df = pd.concat([df1, df2], keys=['file1', 'file2'])

    # 重置索引并添加行号
    merged_df = merged_df.reset_index().rename(columns={'level_0': 'file', 'level_1': 'row_num'})

    template_str = """
    <html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            .added {
                background-color: lightgreen;
            }
            .deleted {
                background-color: red;
            }
        </style>
    </head>
    <body>
        <h1>表格比对结果</h1>
        <table>
            <tr>
                <th>文件</th>
                <th>行号</th>
                {% for column in merged_df.columns %}
                    <th>{{ column }}</th>
                {% endfor %}
            </tr>
            {% for row in merged_df.itertuples() %}
                <tr>
                    <td>{{ row.file }}</td>
                    <td>{{ row.row_num }}</td>
                    {% for column in merged_df.columns[2:] %}
                        {% if row['file'] == 'file1' and row[column] != merged_df.at[row.Index, column.replace('file1', 'file2')] %}
                            <td class="deleted">{{ row[column] }}</td>
                        {% elif row['file'] == 'file2' and row[column] != merged_df.at[row.Index, column.replace('file2', 'file1')] %}
                            <td class="added">{{ row[column] }}</td>
                        {% else %}
                            <td>{{ row[column] }}</td>
                        {% endif %}
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    template = Template(template_str)
    html_content = template.render(merged_df=merged_df)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    compare_tables_to_html('2.xlsm', '1.xlsm', 'diff.html')