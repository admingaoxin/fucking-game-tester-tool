import yaml
from django.db import models

from project.models import Project

# Create your models here.


class Endpoint(models.Model):
    objects: models.QuerySet
    """接口"""
    name = models.CharField("接口名称", max_length=32)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    method = models.CharField("请求方法", max_length=8)
    url = models.CharField("接口地址", max_length=255)
    """参数"""
    params = models.JSONField(
        verbose_name="查询字符串", max_length=10240, blank=True, null=True
    )
    data = models.JSONField(verbose_name="表单", max_length=10240, blank=True, null=True)
    json = models.JSONField(
        verbose_name="JSON参数", max_length=10240, blank=True, null=True
    )
    cookies = models.JSONField(
        verbose_name="Cookies", max_length=10240, blank=True, null=True
    )
    headers = models.JSONField(
        verbose_name="请求头", max_length=10240, blank=True, null=True
    )


class Case(models.Model):
    objects: models.QuerySet
    """接口用例"""
    name = models.CharField("用例名称", max_length=32)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="case_api"
    )
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    allure = models.JSONField(verbose_name="Allure标注", blank=True, null=True)
    """用例步骤，实际传参"""
    api_args = models.JSONField(verbose_name="接口用例参数", blank=True, null=True)
    """数据提取"""
    extract = models.JSONField(verbose_name="数据提取", blank=True, null=True)
    """断言"""
    validate = models.JSONField(verbose_name="断言标注")

    """todo 生成yaml文件"""

    def to_yaml(self, path):
        from .serializers import CaseSerializer

        serializer = CaseSerializer(self)
        data = serializer.data  # json内容
        d = {"test_name": data["name"]}

        d.update(data["allure"])

        d["request"] = {}

        for k, v in data["endpoint_info"].items():
            if v is None:
                continue
            if k not in (
                    "method",
                    "url",
                    "params",
                    "data",
                    "json",
                    "cookies",
                    "headers",
            ):
                continue

            d["request"][k] = v

        for k, v in data['api_args'].items():
            if v:
                d['request'][k].update(v)
        d["extract"] = data["extract"]
        d["validate"] = data["validate"]
        with open(
            path / f"test_{self.id}_{self.name}.yaml", "w", encoding="utf-8"
        ) as f:
            yaml.safe_dump(d, f, allow_unicode=True)
