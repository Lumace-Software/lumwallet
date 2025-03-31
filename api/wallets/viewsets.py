from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Modelo
from .models import Wallet
# Serializador
from .serializers import WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Wallet model.
    """
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Override the get_queryset method to filter wallets by the authenticated user.
        """
        # Get the current authenticated user
        user = self.request.user
        return Wallet.objects.filter(user=user, is_active=True)
    
    def perform_create(self, serializer):
        """
        Set the authenticated user as created_by and updated_by when creating a wallet.
        Also sets the user field if not provided in the request.
        """
        # Get the current authenticated user
        user = self.request.user
        
        # Check if the user field is provided in the request, otherwise use the authenticated user
        if 'user' not in serializer.validated_data:
            serializer.save(created_by=user, updated_by=user, user=user)
        else:
            serializer.save(created_by=user, updated_by=user)
    
    def perform_update(self, serializer):
        """
        Set the authenticated user as updated_by when updating a wallet.
        """
        # Get the current authenticated user
        user = self.request.user
        
        # Only update the updated_by field
        serializer.save(updated_by=user)