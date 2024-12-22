from django.urls import path
from .views import ListCreateMeeting, RetrieveUpdateDestroyMeeting, ListMeeting, RetrieveMeeting

urlpatterns = [
    path("", ListCreateMeeting.as_view(), name="meeting"),
    path("list/", ListMeeting.as_view(), name="meeting_list"),
    path("<int:pk>/", RetrieveUpdateDestroyMeeting.as_view(), name="update"),
    path("<int:pk>/view/", RetrieveMeeting.as_view(), name="view"),
]