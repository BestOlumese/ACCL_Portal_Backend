from django.urls import path
from .views import ListCreateLeave, RetrieveUpdateDestroyLeave, UpdateStatusLeave, ListLeave

urlpatterns = [
    path("", ListCreateLeave.as_view(), name="leave"),
    path("list/", ListLeave.as_view(), name="list_leave"),
    path("<int:pk>/", RetrieveUpdateDestroyLeave.as_view(), name="update"),
    path("<int:pk>/status/", UpdateStatusLeave.as_view(), name="update_status"),
]