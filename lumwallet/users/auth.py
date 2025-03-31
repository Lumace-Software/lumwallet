from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer

# Register a new user
class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for creating a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer