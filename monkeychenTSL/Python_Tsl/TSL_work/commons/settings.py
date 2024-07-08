"""
@Filename:   commons/settings.py
@Author:      北凡
@Time:        2023/5/26 21:33
@Describe:    ...
"""
from selenium.webdriver.common.by import By

# 此文件不允许import 同项目的其他模块


driver_type = "chrome"
wait_max_time = 10
selenium_by = By.XPATH


test_case_path = ""
test_glob = "**/test_*.yaml"

extract_path = "extract.yaml"
rsa_pub_path = "api.pub"

base_url = "http://47.107.116.139"


allure_epic = "自动化测试"
allure_feature = "默认模块"
allure_story = "默认功能"
