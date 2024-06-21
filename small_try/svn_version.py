import subprocess
import pandas as pd
import os
from   import compare_tables_to_html


def get_svn_file(svn_url, revision, output_file):
    command = f'svn export -r {revision} {svn_url} {output_file}'
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    svn_url = 'https://svn.example.com/svn/repo/file.xlsx'
    revision1 = 100
    revision2 = 200

    temp_dir = 'temp_export'
    os.makedirs(temp_dir, exist_ok=True)

    file1 = os.path.join(temp_dir, f'file_revision_{revision1}.xlsx')
    file2 = os.path.join(temp_dir, f'file_revision_{revision2}.xlsx')

    get_svn_file(svn_url, revision1, file1)
    get_svn_file(svn_url, revision2, file2)

    compare_tables_to_html(file1, file2, 'diff.html')

    # 删除临时文件夹
    os.rmdir(temp_dir)
