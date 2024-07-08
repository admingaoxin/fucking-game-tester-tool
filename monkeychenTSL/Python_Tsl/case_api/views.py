from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Case, Endpoint
from .serializers import CaseSerializer, EndpointSerializer


@extend_schema(tags=["Case_api"])
class EndpointViewSet(viewsets.ModelViewSet):
    # 数据从哪里查询
    queryset = Endpoint.objects.all()
    # 数据按照什么样的接口进行响应
    serializer_class = EndpointSerializer


@extend_schema(tags=["Case_api"])
class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
