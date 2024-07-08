from pathlib import Path

from rest_framework import serializers

from .models import RunResult, Suite


class RunResultSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    suite_name = serializers.SerializerMethodField()
    run_type = serializers.SerializerMethodField()
    status = serializers.CharField(source="get_status_display")

    report_url = serializers.SerializerMethodField()
    log_url = serializers.SerializerMethodField()
    artifacts_url = serializers.SerializerMethodField()

    class Meta:
        model = RunResult
        # fields = '__all__'
        exclude = ["path"]

    def get_project_name(self, obj: RunResult):
        return obj.project.name

    def get_suite_name(self, obj: RunResult):
        return obj.suite.name

    def get_run_type(self, obj: RunResult):
        return obj.suite.get_run_type_display()



    def get_report_url(self, obj):
        path = Path(str(obj.path))
        dir_name = path.name
        return f"/api/suite/static/{dir_name}/report/index.html"

    def get_log_url(self, obj):
        path = Path(str(obj.path))
        dir_name = path.name
        return f"/api/suite/static/{dir_name}/logs/pytest.log"

    def get_artifacts_url(self, obj):
        path = Path(str(obj.path))
        dir_name = path.name
        return f"/api/suite/static/{dir_name}/artifacts.zip"


class SuiteSerializer(serializers.ModelSerializer):
    # 项目名称
    project_name = serializers.SerializerMethodField()
    # UI用例数量
    case_ui_count = serializers.IntegerField(read_only=True)
    # API用例数量
    case_api_count = serializers.IntegerField(read_only=True)

    # 用例执行模式
    run_type_display = serializers.CharField(
        read_only=True, source="get_run_type_display"
    )

    schedule = serializers.IntegerField(read_only=True, required=False, allow_null=True)

    class Meta:
        model = Suite
        fields = "__all__"

    def get_project_name(self, obj: Suite):
        return obj.project.name
