from rest_framework import generics
from .serializers import LeaveSerializer, LeaveAdminSerializer
from .models import Leave
from rest_framework.permissions import IsAuthenticated
from backend.permissions import IsSuperUser, IsStaff
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from datetime import timedelta

class ListCreateLeave(generics.ListCreateAPIView):
    queryset = Leave.objects.all().order_by('-created_at')
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Leave.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        # Calculate the leave duration first
        leave = serializer.validated_data
        leave_duration = leave['end_date'] - leave['start_date']

        # Get or create UserProfile for the current user
        user_profile = self.request.user.userprofile
        if user_profile.leaves is None:
            user_profile.leaves = 0  # Initialize to 0 if None

        # Check if the user has enough leaves
        remaining_leaves = user_profile.leaves - leave_duration.days
        if remaining_leaves < 0:
            raise ValidationError("You don't have enough leaves for this duration.")

        # If the user has enough leaves, save the leave and update the balance
        user_profile.leaves = remaining_leaves
        user_profile.save()

        # Save the leave
        serializer.save(user=self.request.user)


class ListLeave(generics.ListAPIView):
    queryset = Leave.objects.all().order_by('-created_at')
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

class ListDirectorLeave(generics.ListAPIView):
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def get_queryset(self):
        user = self.request.user

        # Assuming user profile or a custom role determines if the user is a director
        if user.is_staff:
            return Leave.objects.filter(director=user).order_by('-created_at')
        
        return Leave.objects.none() 

class RetrieveUpdateDestroyLeave(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaveSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Leave.objects.filter(user=user).order_by('-created_at')

    def perform_update(self, serializer):
        leave = self.get_object()  # Fetch the original leave instance before update

        # Check if the leave status is 'approved' and prevent update
        if leave.status == 'approved':
            raise ValidationError("You cannot edit a leave that has already been approved.")

        # Get the original leave duration (before update)
        original_leave_duration = leave.end_date - leave.start_date
        updated_leave_duration = serializer.validated_data['end_date'] - serializer.validated_data['start_date']

        # Get the UserProfile for the current user
        try:
            user_profile = self.request.user.userprofile
        except AttributeError:
            raise Exception("User does not have an associated UserProfile.")

        if user_profile.leaves is None:
            user_profile.leaves = 0  # Initialize to 0 if None

        # Check if the user has enough leaves
        remaining_leaves = user_profile.leaves + original_leave_duration.days - updated_leave_duration.days

        # If the remaining leave balance is 0 or negative, raise an error
        if remaining_leaves <= 0:
            raise ValidationError("You don't have enough leaves for this duration.")

        # Update the leave balance
        user_profile.leaves = remaining_leaves
        user_profile.save()

        # Save the updated leave
        updated_leave = serializer.save()

        # Return a response with success status and updated leave details
        return Response({
            'status': 'success',
            'message': 'Leave updated successfully',
            'data': LeaveSerializer(updated_leave).data
        }, status=status.HTTP_200_OK)

    # Optional: Customize the `destroy` method to prevent deletion if needed
    def perform_destroy(self, instance):
        if instance.status == 'approved':
            raise ValidationError("You cannot delete a leave that has already been approved.")
        instance.delete()

    
class UpdateStatusLeave(generics.UpdateAPIView):
    serializer_class = LeaveAdminSerializer
    lookup_field = "pk"
    queryset = Leave.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated, IsStaff]
