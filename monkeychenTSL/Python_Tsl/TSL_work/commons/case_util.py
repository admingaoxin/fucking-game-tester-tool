"""
@Filename:   commons/case_util
@Author:      北凡
@Time:        2023/5/24 20:54
@Describe:    ...
"""
import logging
from pathlib import Path

import jsonpath
import yaml
from commons import settings
from commons.ddt_util import ddt
from commons.models import CaseInfo
from commons.session import BeifanSession
from commons.yaml_util import YamlUtil
from pytest_yaml.templates import Template

logger = logging.getLogger(__name__)

session = BeifanSession()
yaml_file = YamlUtil(settings.extract_path)

extrac_data = yaml_file.read() or {}

logger.info(f"{extrac_data=}")


def load_case():
    base_path = Path(settings.test_case_path)  # 测试用例的存放目录

    yaml_path_list = list(base_path.glob(settings.test_glob))  # 此列表的内容、顺序，决定用例的内容和顺序
    yaml_path_list.sort()

    logger.info(f"从{base_path} 加载到 {len(yaml_path_list)}个yaml文件：")
    logger.info(f"{yaml_path_list}")

    case_info_list = []  # 用例内容
    case_name_list = []  # 用例名称

    for yaml_path in yaml_path_list:
        data = YamlUtil(yaml_path).read()  # 加载yaml内容

        if isinstance(data, dict):  # 如果data是字典，属于普通用例，每个接口属于各自的用例
            if "parametrize" in data:  # 是否使用数据驱动测试
                for data in ddt(data):  # 进行DDT处理 ：一个用例变成多个用例
                    case_data_to_case_list(data, case_info_list, case_name_list)
            else:
                case_data_to_case_list(data, case_info_list, case_name_list)

        elif isinstance(data, list):
            first_case_info = None  # 首个用例，以它 的名词、allure注解，作为整个用例的名称、注解
            all_case_info = []  # yaml 所有的用例内容
            # data是一个列表 说明此文件是流程用例，多个接口属于同一个用例

            for case_info_data in data:
                try:
                    _case_info = CaseInfo(**case_info_data)  # 校验yaml格式

                    if first_case_info is None:  # 如果没有首个用例，就创建首个用例
                        first_case_info = _case_info

                    all_case_info.append(_case_info)

                    if "bbs" in str(yaml_path):  # 根据路径，自动标注模块
                        _case_info.feature = "论坛模块"
                    elif "weixin" in str(yaml_path):
                        _case_info.feature = "微信模块"

                except Exception as e:
                    raise ValueError(f"{e.args} ({yaml_path})")  # 报错，发出提示

            case_info_list.append(all_case_info)  # yaml中所有的内容，作为一个用例
            case_name_list.append(first_case_info.test_name)  # 将用例名称放入列表

            logger.info(f"{yaml_path} 加载到用例: {first_case_info.test_name}")

    logger.info(f"共加载到用例：{len(case_info_list)}个")
    return case_info_list, case_name_list


def case_data_to_case_list(data, case_info_list, case_name_list):
    _case_info = CaseInfo(**data)  # 校验yaml格式
    case_info_list.append([_case_info])  # yaml中所有的内容，作为一个用例
    case_name_list.append(_case_info.test_name)  # 将用例名称放入列表


def run_case(all_case_info):
    for case_info in all_case_info:
        # 1. request 请求接口
        request = case_info.request  # 字典  -> 字符串  -> 替换变量  -> 字典  ->传参
        request_str = yaml.safe_dump(request, allow_unicode=True)  # 字典转字符串

        # new_request_str = Template(request_str).safe_substitute(extrac_data) # string的Template，只支持变量，不支持函数
        ## pytest-yaml的Template，支持变量，也支持函数
        new_request_str = Template(request_str).render(extrac_data)

        # print(f"{request_str=}")
        # print(f"{new_request_str=}")
        new_request = yaml.safe_load(new_request_str)  # 字符串转字典

        resp = session.request(**new_request)
        try:
            resp.json = resp.json()  # 把带括号的结果，报错到不带括号的属性
        except:
            resp.json = {"msg": "is not json data"}

        # 2. extract 提取返回数据
        if isinstance(case_info.extract, dict):
            for val_name, val_expr in case_info.extract.items():
                attr = getattr(resp, val_expr[0])  # 通过反射+ 表达式第一项，得到全部数据
                # print(attr)

                try:
                    attr = dict(attr)
                except Exception:
                    pass

                # 通过jsonpath+ 表达式第二项，得到指定数据（列表）
                val_value_list = jsonpath.jsonpath(attr, val_expr[1])
                # print(val_value_list)

                if val_value_list:
                    val_value = val_value_list[val_expr[2]]  # 表达式第二项，得到指定数据中的指定数据（单个数据）
                else:
                    val_value = "no data"
                # print(val_name, '=', val_value)
                extrac_data[val_name] = val_value

                logger.info(f"提取到变量 {val_name} = {val_value}")
                yaml_file.write(extrac_data)
                if val_name.startswith("session_"):  # 如果是session级变量
                    params = session.params or {}
                    params[val_name[8:]] = val_value
                    session.params = params  # 赋值给session

        # 3. validate 断言

        for assert_type, assert_expr in case_info.validate.items():
            match assert_type:
                case "equals":
                    logger.info(f"这是相等断言 {assert_expr}")
                    for key, value in assert_expr.items():
                        assert_msg = key  # 断言提示
                        # 字典get方法：根据key取值，如果没有就返回默认值
                        var_value = extrac_data.get(value[0], "no data")
                        attr = getattr(resp, value[0], var_value)  # 反射取值
                        expect = value[1]  # 预期结果

                        # 1. 如果resp有这个这个属性，就返回属性
                        # 2. 如果resp没有这个属性，但是有这个变量，就返回变量
                        # 2. 如果resp没有这个属性，也没有这个变量，就返no data

                        logger.info(f"{attr}== {expect}, {assert_msg}")
                        assert str(attr) == str(expect), assert_msg

                case "contains":
                    logger.info(f"这是包含断言 {assert_expr}")
                    for key, value in assert_expr.items():
                        assert_msg = key  # 断言提示
                        var_value = extrac_data.get(value[0], "no data")
                        attr = getattr(resp, value[0], var_value)  # 反射取值
                        expect = value[1]  # 预期结果

                        logger.info(f"{attr} in {expect}, {assert_msg}")
                        assert expect in attr, assert_msg
