import logging
import time
from typing import Optional

from pytest_yaml.templates import Template
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from . import settings

g_vars = {}
logger = logging.getLogger(__name__)

class KeyWord:
    driver: Optional[Chrome] = None

    def __init__(self, usefixtures):
        self._usefixtures = usefixtures

    def __getattr__(self, item):
        if item == "assert":
            return self._assert
    def set_driver(self, fixture_name, *args):
        """设置默认浏览器"""
        self.driver = self._usefixtures[fixture_name]
    def action_by_driver(self, fixture_name, action_name, *args):
        """通过另一个浏览器执行指定的关键字"""
        driver = self._usefixtures[fixture_name]
        wd = self.__class__(driver)
        func = getattr(wd, action_name)
        func(*args)
    def fixture2driver(self, fixture_name, *args):
        self.driver = self._usefixtures[fixture_name]

    def wait(self, func, *args):
        # 允许任意数量的参数
        return WebDriverWait(self.driver, settings.wait_max_time).until(func)  # 等待 0~5秒

    def find_element(self, by, value, need_text=False, *args):
        def f(driver, *args):  # 自定义
            txt = driver.find_element(by, value).text

            if need_text:  # 如果需要文本
                return txt.replace(" ", "")  # 返回文本进行判断
            else:  # 如果不需要文本
                return True  # 直接成功

        self.wait(f)  # 显式等待

        return self.driver.find_element(by, value)  # 返回元素

    def goto(self, url, *args):
        self.driver.get(url)

    def click(self, loc: str, *args):
        el = self.find_element(By.XPATH, loc)
        el.click()

    def input(self, loc: str, content="", *args):
        el = self.find_element(settings.selenium_by, loc)
        el.send_keys(content)

    def save_text(self, loc: str, var_name, need_text=True, *args):
        def f(x, *args):
            e = self.driver.find_element(settings.selenium_by, loc)
            t = e.text.replace(" ", "")
            if t:  # 文本是否包含非空字符串
                return t
            else:
                return False

        if need_text:  # 必须要有内容
            text = self.wait(f)
        else:
            text = self.find_element(settings.selenium_by, loc).text

        g_vars[var_name] = text
        return text

    def iframe_enter(self, loc, *args):
        el = self.find_element(settings.selenium_by, loc)
        self.driver.switch_to.frame(el)

    def iframe_exit(self, *args):
        self.driver.switch_to.default_content()

    def select(self, loc, text, *args):
        select = Select(self.driver.find_element(settings.selenium_by, loc))
        select.select_by_visible_text(text)  # 选择哪一个提示内容

    def clear(self, loc, *args):
        el = self.find_element(settings.selenium_by, loc)
        el.clear()

    def js_code(self, loc, code, *args):
        el = self.find_element(settings.selenium_by, loc)
        self.driver.execute_script(code, el)

    def sleep(self, x, *args):
        time.sleep(x)

    def _assert(self, a, contrast, b):
        logger.info(f"开始断言:  {a} {contrast} {b}")

        a = Template(a).render(g_vars)
        b = Template(b).render(g_vars)

        match contrast:
            case "equal":
                logger.info(f"{a} == {b}")
                assert a == b
            case "contains":
                logger.info(f"{a} in {b}")
                assert a in b
            case _:
                logger.error("未知的断言方式")
                assert False, "未知的断言方式"

    def asser_text(self, loc: str, text: str, *args):
        el_text = self.get_text(loc)  # 页面中文本

        assert el_text == text

    def assert_value(self, loc: str, value: str, *args):
        el = self.find_element(settings.selenium_by, loc)
        el_value = el.get_attribute("value")

        assert el_value == value

    def to_mq(self, method, url, data):
        resp = "123"  # 使用requests得到接口响应
        # 把响应，写入到 elements.yaml
        # 调用mq写入内容


