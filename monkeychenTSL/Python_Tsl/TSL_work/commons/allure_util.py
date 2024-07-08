"""
@Filename:   commons/allure_util
@Author:      北凡
@Time:        2023/5/24 20:51
@Describe:    ...
"""
import logging

import allure

logger = logging.getLogger(__name__)


def set_allure_info(all_case_info):
    first_case_info = all_case_info[0]

    l = []

    if first_case_info.epic:
        allure.dynamic.epic(first_case_info.epic)
        l.append("epci")

    if first_case_info.feature:
        allure.dynamic.feature(first_case_info.feature)
        l.append("feature")

    if first_case_info.story:
        allure.dynamic.story(first_case_info.story)
        l.append("story")

    if first_case_info.title:
        allure.dynamic.title(first_case_info.title)
        l.append("title")

    else:
        allure.dynamic.title(first_case_info.test_name)
        l.append("title")

    logger.info(f"设置了以下allure标注: {l}")
