from rest_framework import routers

from .views import DepartmentViewSet, PositionViewSet, RoleViewSet

router = routers.SimpleRouter()

router.register(
    "department",
    DepartmentViewSet,
)
router.register(
    "position",
    PositionViewSet,
)
router.register(
    "role",
    RoleViewSet,
)
urlpatterns = router.urls
