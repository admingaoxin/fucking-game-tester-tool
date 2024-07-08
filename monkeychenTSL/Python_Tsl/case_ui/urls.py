from rest_framework import routers

from .views import CaseViewSet, ElementViewSet

router = routers.SimpleRouter()

router.register(
    "element",
    ElementViewSet,
)
router.register(
    "case",
    CaseViewSet,
)
urlpatterns = router.urls
