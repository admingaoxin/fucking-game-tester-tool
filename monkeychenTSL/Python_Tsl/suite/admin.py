from django.contrib import admin
from .models import Suite,RunResult

# 注册模型以在管理后台中显示它们
admin.site.register(Suite)
admin.site.register(RunResult)