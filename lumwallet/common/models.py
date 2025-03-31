from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BaseModel(models.Model):
    """
    Base model for all models in the application.
    """
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the object was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the object was last updated")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by', null=False, blank=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=False, blank=False)
    is_active = models.BooleanField(default=True, help_text="Indicates if the object is active or not")
    class Meta:
        abstract = True