from django.db import models
from rest_framework.authtoken.admin import User


class Department(models.Model):
    """部门"""

    objects: models.QuerySet
    name = models.CharField("部门名称", max_length=32)
    intro = models.CharField("部门简介", max_length=256, default="")
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)


class Position(models.Model):
    """职位"""

    objects: models.QuerySet
    name = models.CharField("职位名称", max_length=32)
    is_leader = models.BooleanField("负责人", default=False)


class Role(models.Model):
    """角色"""

    objects: models.QuerySet
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
