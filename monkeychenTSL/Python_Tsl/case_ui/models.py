import openpyxl
from django.db import models
from selenium.webdriver.common.by import By

from project.models import Project

by_list = []

for attr in dir(By):
    if attr.startswith("_"):
        continue
    by_list.append((attr, attr))


class Element(models.Model):
    objects: models.QuerySet
    """UI"""
    name = models.CharField("元素名称", max_length=32)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    by = models.CharField("定位方式", choices=by_list, default="XPATH", max_length=20)
    value = models.CharField("定位表达式", max_length=255)


class Case(models.Model):
    objects: models.QuerySet
    """UI用例"""
    name = models.CharField("用例名称", max_length=32)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="case_ui"
    )
    usefixtures = models.JSONField(verbose_name="fixture列表", blank=True, null=True)
    steps = models.JSONField(verbose_name="用例步骤", blank=True, null=True)

    def to_xlsx(self, path):
        """生成excel文件"""
        from .serializers import CaseUISerializer

        serializer = CaseUISerializer(self)
        json_data = serializer.data  # json内容

        xlsx_data = []
        xlsx_data.append(
            [
                "步骤",
                "步骤名",
                "关键字",
                "参数",
            ]
        )
        xlsx_data.append(["-1", "用例名称", "name", json_data["name"]])
        xlsx_data.append(
            [
                "-1",
                "申明fixture",
                "mark",
                "usefixtures",
                ",".join(json_data["usefixtures"]),
            ]
        )

        for step in json_data["steps"]:
            _BlankField = step.pop("_BlankField", [])
            fields = list(step.values())
            fields.extend(_BlankField)
            xlsx_data.append(fields)

        for d in xlsx_data:
            print(d)

        wb = openpyxl.Workbook()
        ws = wb.active

        for d in xlsx_data:
            ws.append(d)

        wb.save(path / f"test_{self.id}_{self.name}.xlsx")
