from rest_framework import routers

from .views import ConfigViewSet, ProjectViewSet

router = routers.SimpleRouter()

router.register(
    "project",
    ProjectViewSet,
)
router.register(
    "config",
    ConfigViewSet,
)
urlpatterns = router.urls
