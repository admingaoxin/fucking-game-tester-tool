from rest_framework import serializers

from account.models import Profile
from .models import Department, Position, Role


class DepartmentSerializer(serializers.ModelSerializer):
    leader_img = serializers.SerializerMethodField()
    leader_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = "__all__"  # 使用全部字段

    def get_leader_img(self, obj: Department):
        if obj.leader:
            from account.models import Profile
            profile, _ = Profile.objects.get_or_create(user=obj.leader)
            if profile.head_img:
                return profile.head_img
            elif profile.name:
                return profile.name
            else:
                return obj.leader.username
        else:
            return ""

    def get_leader_name(self, obj: Department):
        if obj.leader:
            return obj.leader.username
        else:
            return ""


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"  # 使用全部字段


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"  # 使用全部字段


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"  # 使用全部字段


class RoleSystemSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")  # 部门的名称
    position = PositionSerializer()  # 职位的名称
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = "__all__"  # 使用全部字段

    def get_user_profile(self, obj) -> UserProfileSerializer:
        profile, _ = Profile.objects.get_or_create(user=obj.user)
        return UserProfileSerializer(profile).data
