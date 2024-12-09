from rest_framework import serializers
from .models import Meeting
from rest_framework.exceptions import ValidationError
# from django.utils.timezone import make_aware
# from datetime import datetime
    
class MeetingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = Meeting
        fields = ["id", "title", "content", "day", "start_time", "end_time", "extra_notes", "username", "room", "room_name", "created_at"]
        extra_kwargs = {"username": {"read_only": True}}

    def validate(self, data):
        # Get the current meeting instance to compare against the proposed changes
        instance = self.instance
        day = data.get('day', instance.day if instance else None)
        start_time = data.get('start_time', instance.start_time if instance else None)
        end_time = data.get('end_time', instance.end_time if instance else None)
        user = self.context["request"].user

        # Only check for overlapping meetings if the start or end time is being changed
        if start_time and end_time:  # Check only if both start_time and end_time are provided
            if instance:  # During updates
                if start_time != instance.start_time or end_time != instance.end_time:
                    overlapping_meetings = Meeting.objects.filter(
                        user=user,
                        day=day,
                        start_time__lt=end_time,
                        end_time__gt=start_time
                    ).exclude(id=instance.id)  # Exclude the current instance to avoid self-conflict

                    if overlapping_meetings.exists():
                        raise serializers.ValidationError("This meeting overlaps with an existing meeting.")
            else:  # During creation
                overlapping_meetings = Meeting.objects.filter(
                    user=user,
                    day=day,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )

                if overlapping_meetings.exists():
                    raise serializers.ValidationError("This meeting overlaps with an existing meeting.")

        # Ensure meeting times are in the correct order (start < end)
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be later than start time.")
        
        return data