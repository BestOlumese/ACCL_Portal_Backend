from django.urls import path
from .views import ListCreateRoom, ListRoom, RetrieveUpdateDestroyRoom

urlpatterns = [
    path("", ListCreateRoom.as_view(), name="room"),
    path("list/", ListRoom.as_view(), name="list_room"),
    path("<int:pk>/", RetrieveUpdateDestroyRoom.as_view(), name="update"),
]