from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Profile, HeadImage
from .serializers import (LoginSerializer, ProfileSerializer,
                          Resetpassserializer, HeadImageSerializer, UserListSerializer)


@extend_schema(
    tags=[
        "Account",
    ]
)
# Create your views here.
class ProfileViewset(viewsets.GenericViewSet):
    @extend_schema(
        request=LoginSerializer,
        responses=ProfileSerializer,
    )
    @action(methods=["POST"], detail=False, permission_classes=[permissions.AllowAny])
    def login(self, request):
        # 生成登录的序列化的对象
        serializer = LoginSerializer(data=request.data)
        # 委托给序列化器进行参数校验
        serializer.is_valid(raise_exception=True)
        # 在数据库获取到校验以后的user的数据
        profile = Profile.objects.get(user=serializer.validated_data["user"])
        # 委托给序列化进行字段和数据生成
        serializer = ProfileSerializer(profile)
        # 返回生成的数据
        return Response(serializer.data)

    @extend_schema(
        request=Resetpassserializer,
        responses={204: None},
    )
    @action(methods=["POST"], detail=False)
    def reset_password(self, request):
        # 生成登录的序列化的对象
        serializer = Resetpassserializer(data=request.data)
        # 委托给序列化器进行参数校验
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses=ProfileSerializer,
    )
    @action(methods=["GET"], detail=False)
    def profile(self, request):
        """查询单个数据，返还单个数据"""
        profile, _ = Profile.objects.get_or_create(user=request.user)
        # 委托给序列化进行字段和数据生成
        serializer = ProfileSerializer(profile)
        # 返回生成的数据
        return Response(serializer.data)

    @extend_schema(
        request=ProfileSerializer,
        responses=ProfileSerializer,
    )
    @action(methods=["POST"], detail=False)
    def change(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        # 将请求数据和model数据进行合并
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        request=HeadImageSerializer,
        responses=HeadImageSerializer,
    )
    @action(methods=["POST"], detail=False)
    def img_upload(self, request):
        obj = HeadImage.objects.create(user=request.user)  # 创建model记录
        serializer = HeadImageSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # 修改model记录
        return Response(serializer.data)

    @extend_schema(responses=UserListSerializer)
    @action(methods=["GET"], detail=False)
    def all_user(self, request):
        """查询多个数据，返回多个数据"""
        user_list = Profile.objects.all()  # 查询全部数据
        serializer = UserListSerializer(user_list, many=True)  # 多个数据进行返回
        return Response(serializer.data)  # 委托给序列化进行字段和数据生成
