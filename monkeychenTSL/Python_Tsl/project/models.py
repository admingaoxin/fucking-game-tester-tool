from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """项目"""

    objects: models.QuerySet
    name = models.CharField("项目名称", max_length=32)
    intro = models.CharField("项目简介", max_length=256, default="")
    url = models.CharField("项目地址", max_length=256, default="")
    user_list = models.ManyToManyField(User, blank=True, related_name="project_set")
    pm = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="project_pm_list",
    )


class Config(models.Model):
    objects: models.QuerySet
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    conftest = models.TextField("pytest配置脚本", default="")
