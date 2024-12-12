from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room
from backend.permissions import IsSuperUser
from rest_framework.permissions import IsAuthenticated

class ListCreateRoom(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializer
    permission_classes = [IsSuperUser]

class ListRoom(generics.ListAPIView):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
        
class RetrieveUpdateDestroyRoom(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    lookup_field = "pk"
    queryset = Room.objects.all().order_by('-created_at')
    permission_classes = [IsSuperUser]