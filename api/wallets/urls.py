from rest_framework import routers
from django.urls import path, include
from .viewsets import WalletViewSet

router = routers.DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallets')
urlpatterns = [
    path('api/', include(router.urls)),
]