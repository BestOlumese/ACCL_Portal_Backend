from rest_framework import generics
from .serializers import LeaveSerializer, LeaveAdminSerializer
from .models import Leave
from rest_framework.permissions import IsAuthenticated
from backend.permissions import IsSuperUser

# Create your views here.
class ListCreateLeave(generics.ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Leave.objects.filter(user=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class ListLeave(generics.ListAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

class RetrieveUpdateDestroyLeave(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaveSerializer
    lookup_field = "pk"
    queryset = Leave.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Leave.objects.filter(user=user)
    
class UpdateStatusLeave(generics.UpdateAPIView):
    serializer_class = LeaveAdminSerializer
    lookup_field = "pk"
    queryset = Leave.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]
