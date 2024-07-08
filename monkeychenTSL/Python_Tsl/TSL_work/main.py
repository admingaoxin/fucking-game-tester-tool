"""
@Filename:   /main
@Author:      北凡
@Time:        2023/5/7 20:14
@Describe:    ...
"""

import datetime
import os
import pathlib
import shutil

import pytest
import yaml

pytest.main()  # 启动测试框架

os.system("allure generate -o report temps --clean")  # 生成测试报告

log_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

shutil.move("logs/pytest.log", f"logs/{log_name}.log")

log_list = list(pathlib.Path("logs").glob("*.log"))
log_list.sort()
log_list.reverse()

for log in log_list[3:]:  # 超过三个日志文件，就删除
    log.unlink()
