from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import RunResultViewSet, SuiteViewSet, static_server

router = SimpleRouter()

router.register("run_result", RunResultViewSet)
router.register("suite", SuiteViewSet)
urlpatterns = [
    path("static/<path:path>", static_server, {"document_root": "upload_yaml"})  # 传参成功
]
urlpatterns += router.urls
