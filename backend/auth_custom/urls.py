from django.urls import path
from .views import CreateUserView, CustomTokenObtainPairView, CustomTokenRefreshView, ListDirector, RetrieveUser

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("directors/", ListDirector.as_view(), name="directors"),
    path("remaining/<int:pk>/", RetrieveUser.as_view(), name="user"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]