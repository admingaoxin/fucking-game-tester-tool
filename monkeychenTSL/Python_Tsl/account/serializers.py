from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from system.models import Role

from .models import Profile, HeadImage


class RoleAccountSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    position = serializers.CharField(source="position.name")
    is_leader = serializers.BooleanField(source="position.is_leader")

    class Meta:
        model = Role
        fields = ["department", "position", "is_leader"]  # 使用全部字段


class ProfileSerializer(serializers.ModelSerializer):
    # 序列化器里边增加字段
    token = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    role_list = RoleAccountSerializer(read_only=True, many=True, source="get_role_list")

    class Meta:
        model = Profile
        fields = "__all__"

    def get_token(self, obj):
        user = obj.user
        token, is_create = Token.objects.get_or_create(user=user)
        return token.key

    def get_user(self, obj):
        return obj.user_id


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    # 只校验当前字典
    def validate_username(self, data):
        return data

    # 只校验当前字典
    def validate_password(self, data):
        return data

    # 校验全部字段
    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("用户名或密码不正确")
        else:
            Profile.objects.get_or_create(user=user)  # 为用户创建 个人资料

            Token.objects.get_or_create(user=user)  # 为用户创建 Token

            attrs["user"] = user

            return attrs


class Resetpassserializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=6)
    confirm_password = serializers.CharField(required=True, min_length=6)

    def validate(se1f, attrs):
        # 校验全部字段
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]
        if new_password != confirm_password:
            raise serializers.ValidationError("密码和确认密码不一致")
        return attrs


class HeadImageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = HeadImage
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.id


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
