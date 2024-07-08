from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Config, Project
from .serializers import ConfigSerializer, ProjectSerializer


@extend_schema(tags=["Project"])
class ProjectViewSet(viewsets.ModelViewSet):
    # 数据从哪里查询
    queryset = Project.objects.all()
    # 数据按照什么样的接口进行响应
    serializer_class = ProjectSerializer


@extend_schema(tags=["Project"])
class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
