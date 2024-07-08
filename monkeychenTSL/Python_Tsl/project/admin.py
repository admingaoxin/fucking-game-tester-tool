from django.contrib import admin
from .models import Project,Config

# 注册模型以在管理后台中显示它们
admin.site.register(Project)
admin.site.register(Config)