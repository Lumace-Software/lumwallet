from rest_framework import routers
from .auth import UserViewSet
from django.urls import path, include
router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
]
