from django.urls import path
from .views import ListCreateLeave, RetrieveUpdateDestroyLeave, UpdateStatusLeave, ListLeave, ListDirectorLeave

urlpatterns = [
    path("", ListCreateLeave.as_view(), name="leave"),
    path("list/", ListLeave.as_view(), name="list_leave"),
    path("directorlist/", ListDirectorLeave.as_view(), name="list_director_leave"),
    path("<int:pk>/", RetrieveUpdateDestroyLeave.as_view(), name="update"),
    path("<int:pk>/status/", UpdateStatusLeave.as_view(), name="update_status"),
]