from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, RetrieveUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import UserProfile


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ListDirector(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter the queryset to return only users where is_staff is True
        return User.objects.filter(is_staff=True)
    
class RetrieveUser(generics.RetrieveAPIView):
    serializer_class = RetrieveUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    queryset = User.objects.all()

    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
