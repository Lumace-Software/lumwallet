from rest_framework import serializers
from django.contrib.auth.models import User

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user