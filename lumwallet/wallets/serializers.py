from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wallet model.
    """
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by', 'user']