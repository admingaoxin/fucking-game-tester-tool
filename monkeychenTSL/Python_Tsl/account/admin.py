from django.contrib import admin
from .models import Profile,HeadImage

# 注册模型以在管理后台中显示它们
admin.site.register(Profile)
admin.site.register(HeadImage)
