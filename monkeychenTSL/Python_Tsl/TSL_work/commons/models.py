"""
@Filename:   commons/models
@Author:      北凡
@Time:        2023/5/19 20:27
@Describe:    ...
"""

from dataclasses import dataclass

from commons import settings


@dataclass
class CaseInfo:
    test_name: str

    request: dict
    validate: dict
    parametrize: list = None
    extract: dict = None
    epic: str = settings.allure_epic
    feature: str = settings.allure_feature
    story: str = settings.allure_story
    title: str = None

    def __repr__(self):
        return str(id(self))
