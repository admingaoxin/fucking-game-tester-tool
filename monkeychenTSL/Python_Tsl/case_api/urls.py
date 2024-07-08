from rest_framework import routers

from .views import CaseViewSet, EndpointViewSet

router = routers.SimpleRouter()

router.register(
    "endpoint",
    EndpointViewSet,
)
router.register(
    "case",
    CaseViewSet,
)
urlpatterns = router.urls
