from django.contrib import admin
from .models import Endpoint,Case

# 注册模型以在管理后台中显示它们
admin.site.register(Endpoint)
admin.site.register(Case)