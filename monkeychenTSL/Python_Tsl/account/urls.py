from django.urls import path
from django.views.static import serve
from rest_framework import routers

from .models import app_static_path
from .views import ProfileViewset

router = routers.SimpleRouter()

router.register("profile", ProfileViewset, basename="profile")

urlpatterns = [path("static/<path:path>", serve, {"document_root": app_static_path})]

urlpatterns += router.urls
