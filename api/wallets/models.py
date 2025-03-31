from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.

class Wallet(BaseModel):
    # A wallet is a collection of assets
    name = models.CharField(max_length=100, blank=False, null=False, help_text="Wallet name")
    description = models.TextField(blank=True, null=True, help_text="Wallet description")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets', help_text="User who owns the wallet")
    
    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        db_table = "wallets"
