from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Department, Position, Role
from .serializers import (DepartmentSerializer, PositionSerializer,
                          RoleSystemSerializer,RoleSerializer)






@extend_schema(tags=["System"])
class DepartmentViewSet(viewsets.ModelViewSet):
    # 数据从哪里查询
    queryset = Department.objects.all()
    # 数据按照什么样的接口进行响应
    serializer_class = DepartmentSerializer



@extend_schema(tags=["System"])
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


@extend_schema(tags=["System"])
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    @extend_schema(responses=RoleSystemSerializer)
    def list(self, request, *args, **kwargs):
        self.serializer_class = RoleSystemSerializer
        return super().list(request, *args, **kwargs)