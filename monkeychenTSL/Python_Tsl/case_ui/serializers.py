from rest_framework import serializers

from project.models import Project
from .models import Case, Element


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"  # 使用全部字段


class ElementSerializer(serializers.ModelSerializer):
    project_info = ProjectSerializer(source="project", read_only=True)

    class Meta:
        model = Element
        fields = "__all__"  # 使用全部字段


class UIstepSerializer(serializers.Serializer):
    序号 = serializers.CharField()
    步骤名 = serializers.CharField()
    关键字 = serializers.CharField()
    参数 = serializers.CharField()
    _BlankField = serializers.ListField(allow_null=True,required=False,default=[])


class CaseUISerializer(serializers.ModelSerializer):
    project_info = ProjectSerializer(source="project", read_only=True)
    usefixtures = serializers.ListField()
    steps = UIstepSerializer(many=True,required=False,default=[])

    class Meta:
        model = Case
        fields = "__all__"  # 使用全部字段
