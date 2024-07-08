# import time
# from pathlib import Path

from django.views.static import serve
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
# from .tasks import ThreadPoolExecutor, run_pytest
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

# from django.contrib.auth.decorators import login_required
# rest_framework.permissions.IsAuthenticated
from .models import RunResult, Suite
from .serializers import RunResultSerializer, SuiteSerializer

# from case_api.models import Case as CaseAPI
# from case_ui.models import Case as CaseUI


@api_view()  # drf的接口
def static_server(request, path, document_root=None, show_indexes=False):
    resp = serve(request, path, document_root, show_indexes)

    # 修改响应头
    if resp.status_code == 200:
        if path.endswith(".yaml") or path.endswith(".log"):
            resp.headers["Content-Type"] = "text/css; charset=utf-8"

    return resp


@extend_schema(tags=["Suite"])
class SuiteViewSet(viewsets.ModelViewSet):
    # 数据从哪里查询
    queryset = Suite.objects.all()
    # 数据按照什么样的接口进行响应
    serializer_class = SuiteSerializer

    @action(methods=["POST"], detail=True)
    def run(self, request, pk):
        """执行测试套件"""
        obj: Suite = self.get_object()
        if obj.run_type == obj.RunType.ONCE:
            result = obj.run()
            return Response({"result_id": result.id})
        else:
            return Response(
                {"detail": f"套件不允许手动触发，运行类型={obj.run_type}"}, status=400
            )

    # 去掉鉴权机制，只针对此接口
    @action(
        methods=["POST", "GET"], detail=True, permission_classes=[permissions.AllowAny]
    )
    def webhook(self, request, pk):
        """执行测试套件"""
        obj: Suite = self.get_object()
        hook_key = request.query_params.get("key")
        if obj.run_type == obj.RunType.WebHook:
            if hook_key == obj.hook_key:
                result = obj.run()
                return Response({"result_id": result.id})
            else:
                return Response({"result_id": -2, "msg": "WebHook的Key不正确"}, status=400)
        else:
            return Response(
                {"result_id": -1, "msg": f"套件不允许WebHook触发，运行类型={obj.run_type}"}
            )


@extend_schema(tags=["Suite"])
class RunResultViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = RunResult.objects.all().order_by("-id")
    serializer_class = RunResultSerializer

    # @action(methods=['POST'], detail=True)
    # def run_case_api(self, request, pk):
    #     """调试接口，临时运行测试框架"""
    #
    #     obj: CaseAPI = CaseAPI.objects.get(id=pk)  # 得到用例的对象
    #
    #     path = Path("upload_yaml") / f"{pk}_{time.time()}"  # 创建绝不重名的目录名
    #     path.mkdir(parents=True, exist_ok=True)  # 创建目录
    #
    #     obj.to_yaml(path)
    #
    #     pool = ThreadPoolExecutor(max_workers=6)  # 8-2
    #     pool.map(run_pytest, [path])
    #     return Response({"id": pk, "path": str(path)})
    #
    # @action(methods=['POST'], detail=True)
    # def run_case_ui(self, request, pk):
    #     """调试接口，临时运行测试框架"""
    #
    #     obj: CaseUI = CaseUI.objects.get(id=pk)  # 得到用例的对象
    #
    #     path = Path("upload_yaml") / f"{pk}_{time.time()}"  # 创建绝不重名的目录名
    #     path.mkdir(parents=True, exist_ok=True)  # 创建目录
    #
    #     obj.to_xlsx(path)
    #
    #     pool = ThreadPoolExecutor(max_workers=6)  # 8-2
    #     pool.map(run_pytest, [path])
    #     return Response({"id": pk, "path": str(path)})
