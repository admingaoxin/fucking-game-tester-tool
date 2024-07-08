from pathlib import Path

from django.contrib.auth.models import User
from django.db import models

from system.models import Role

app_path = Path(__file__).parent
app_static_path = app_path / "static"


def user_head_img_path(obj, filename):
    return f"{app_static_path}/user_{obj.user.id}/{filename}"  # 绝对路径

    # Create your models here.


class HeadImage(models.Model):
    objects: models.QuerySet
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.FileField("头像内容", upload_to=user_head_img_path)#保存图片内容


class Profile(models.Model):
    """个人资料"""

    objects: models.QuerySet
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("昵称", max_length=32)
    head_img = models.CharField("头像地址", max_length=512)  # 保存图片地址

    def get_role_list(self):
        role_list = Role.objects.filter(user=self.user)
        return role_list
