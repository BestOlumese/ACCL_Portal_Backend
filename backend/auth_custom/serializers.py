from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Decode the refresh token
        refresh = RefreshToken(attrs['refresh'])
        user_id = refresh.get('user_id')

        # Fetch the user instance
        User = get_user_model()
        user = User.objects.get(id=user_id)

        # Add custom claims to the new access token
        access = refresh.access_token
        access['is_superuser'] = user.is_superuser
        access['is_staff'] = user.is_staff
        access['username'] = user.username
        access['first_name'] = user.first_name
        access['last_name'] = user.last_name

        # Include the updated access token in the response
        data['access'] = str(access)
        return data
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims
        data['is_superuser'] = self.user.is_superuser
        data['is_staff'] = self.user.is_staff
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password"]
        extra_kwargs = {"password": { "write_only": True }}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class RetrieveUserSerializer(serializers.ModelSerializer):
    leaves = serializers.CharField(source='userprofile.leaves', read_only=True)
    total_leaves = serializers.CharField(source='userprofile.total_leaves', read_only=True)
    class Meta:
        model = User
        fields = ["leaves", "total_leaves"]