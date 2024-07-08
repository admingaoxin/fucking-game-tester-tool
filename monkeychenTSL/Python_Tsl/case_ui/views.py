from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Case, Element
from .serializers import CaseUISerializer, ElementSerializer


@extend_schema(tags=["Case_UI"])
class ElementViewSet(viewsets.ModelViewSet):
    # 数据从哪里查询
    queryset = Element.objects.all()
    # 数据按照什么样的接口进行响应
    serializer_class = ElementSerializer


@extend_schema(tags=["Case_UI"])
class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseUISerializer
