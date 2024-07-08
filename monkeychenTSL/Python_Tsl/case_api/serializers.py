from rest_framework import serializers

from .models import Case, Endpoint


class EndpointSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Endpoint
        fields = "__all__"  # 使用全部字段

    def get_project_name(self, obj: Endpoint):
        return obj.project.name


class CaseSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    endpoint_info = EndpointSerializer(source="endpoint",read_only=True,allow_null=True)

    class Meta:
        model = Case
        fields = "__all__"  # 使用全部字段
    def get_project_name(self, obj: Endpoint):
        return obj.project.name