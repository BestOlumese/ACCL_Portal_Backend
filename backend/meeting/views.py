from rest_framework import generics
from .serializers import MeetingSerializer
from .models import Meeting
from rest_framework.permissions import IsAuthenticated

class ListCreateMeeting(generics.ListCreateAPIView):
    queryset = Meeting.objects.all().order_by('-created_at')
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class ListMeeting(generics.ListAPIView):
    queryset = Meeting.objects.all().order_by('-created_at')
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
        
class RetrieveUpdateDestroyMeeting(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    lookup_field = "pk"
    queryset = Meeting.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(user=user).order_by('-created_at')
    
class RetrieveMeeting(generics.RetrieveAPIView):
    serializer_class = MeetingSerializer
    lookup_field = "pk"
    queryset = Meeting.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]