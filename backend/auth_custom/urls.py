from django.urls import path
from .views import CreateUserView, CustomTokenObtainPairView, CustomTokenRefreshView, ListDirector

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("directors/", ListDirector.as_view(), name="directors"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]