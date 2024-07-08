from django.contrib import admin
from .models import Department,Position,Role

# 注册模型以在管理后台中显示它们
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Role)