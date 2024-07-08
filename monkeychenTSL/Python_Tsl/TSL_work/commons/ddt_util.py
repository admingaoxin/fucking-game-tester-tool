"""
@Filename:   commons/ddt_utile
@Author:      北凡
@Time:        2023/5/24 21:49
@Describe:    ...
"""
import logging

import yaml
from pytest_yaml.templates import Template

logger = logging.getLogger(__name__)


def ddt(data: dict) -> list:
    parametrize = data.pop("parametrize", [])

    keys = parametrize[0]
    parametrize = parametrize[1:]

    logger.info(f"ddt keys = {keys}, len = {len(parametrize)}")

    data_list = []

    for d in parametrize:  # 根据parametrize数量，决定返回的用例的数量
        # d 是列表，要变成字典
        d = dict(zip(keys, d))

        logger.info(f"ddt data={d}")

        # data -> data_str  字典变yaml字符串
        data_str = yaml.safe_dump(data, allow_unicode=True)

        # data_str 借助Template 输入变量，得到new_data_str
        new_data_str = Template(data_str).safe_substitute(d)  # 注入了d数据的用例

        # new_data_str -> new_data  yaml字符串变字典
        new_data = yaml.safe_load(new_data_str)

        data_list.append(new_data)

    print("ddt后的数据", data_list)
    return data_list
