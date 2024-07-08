"""
@Filename:   /conftest
@Author:      北凡
@Time:        2023/8/20 20:19
@Describe:    ...
"""
import allure
import pytest
from commons.kdt import KeyWord
from pytest_xlsx.file import XlsxItem
from selenium import webdriver


def pytest_xlsx_run_step(item: XlsxItem):
    if not hasattr(item, "kw"):
        item.kw = KeyWord(item.usefixtures)  # 同一个用例的不同步骤，使用同一个关键字类

    data = item.current_step  # 步骤内容

    key = data["关键字"]
    args = [
        data["参数"],
    ]  # 列表
    args.extend(data["_BlankField"])
    remark = data["步骤名"]

    # 通过反射 从kw中找到关键字并执行
    f = getattr(item.kw, key)
    f(*args)

    if item.kw.driver:
        png = item.kw.driver.get_screenshot_as_png()  # 二进制
        allure.attach(png, remark, allure.attachment_type.PNG)

    return 1


@pytest.fixture(scope="class")
def chrome():
    from selenium.webdriver import Chrome, ChromeOptions
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-site-isolation-trials')
    options.add_argument('--lang=zh-CN')
    options.add_argument('--window-size=1920,1080')
    driver = Chrome(options=options)

    driver.get('https://www.baidu.com')
    driver.get_screenshot_as_file("page.png")

    print(driver.title)
    print("ok")

    yield driver

    driver.quit()
