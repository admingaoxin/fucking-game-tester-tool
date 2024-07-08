from rest_framework import serializers
from .models import Config, Project
from account.models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"  # 使用全部字段


class ProjectSerializer(serializers.ModelSerializer):
    pm_profile = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"  # 使用全部字段

    def get_pm_profile(self, obj: Project):
        if obj.pm:
            profile, _ = Profile.objects.get_or_create(user=obj.pm)
            return UserProfileSerializer(profile).data


class ConfigSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Config
        fields = "__all__"  # 使用全部字段

    def get_project_name(self, obj: Config):
        return obj.project.name
