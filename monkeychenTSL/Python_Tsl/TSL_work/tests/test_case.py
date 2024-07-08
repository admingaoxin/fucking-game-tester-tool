"""
@Filename:   tests/test_case
@Author:      北凡
@Time:        2023/5/17 20:23
@Describe:    yaml和pytest的连接点
"""

import pytest
from commons.allure_util import set_allure_info
from commons.case_util import load_case, run_case

# 1. 要能一次性加载多个文件，不能把yaml文件名写死
case_info_list, case_name_list = load_case()

print("用例数量:", len(case_info_list))
print("用例内容:", case_info_list)


# 2. 生成yaml相同数量的测试用例
@pytest.mark.parametrize(
    "all_case_info",
    case_info_list,
    ids=case_name_list,
)
def test_(all_case_info):
    set_allure_info(all_case_info)  # 1. 设置allure报告定制
    run_case(all_case_info)  # 2. 执行接口请求和断言
