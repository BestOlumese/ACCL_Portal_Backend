from rest_framework import serializers
from .models import Meeting
from rest_framework.exceptions import ValidationError
# from django.utils.timezone import make_aware
# from datetime import datetime
    
class MeetingSerializer(serializers.ModelSerializer):
    user_firstname = serializers.CharField(source='user.first_name', read_only=True)
    user_lastname = serializers.CharField(source='user.last_name', read_only=True)
    user_name = serializers.SerializerMethodField()  
    
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = Meeting
        fields = ["id", "title", "content", "day", "start_time", "end_time", "extra_notes", "user_firstname", "user_lastname", "user_name", "room", "room_name", "created_at"]
        extra_kwargs = {"username": {"read_only": True}}

    def get_user_name(self, obj):
        # Combine the first and last name for the user
        return f"{obj.user.first_name} {obj.user.last_name}"

    def validate(self, data):
        # Get the current meeting instance to compare against the proposed changes
        instance = self.instance
        day = data.get('day', instance.day if instance else None)
        room = data.get('room', instance.room if instance else None)
        start_time = data.get('start_time', instance.start_time if instance else None)
        end_time = data.get('end_time', instance.end_time if instance else None)
        user = self.context["request"].user

        # Only check for overlapping meetings if the start or end time is being changed
        if start_time and end_time:  # Check only if both start_time and end_time are provided
            if instance:  # During updates
                if start_time != instance.start_time or end_time != instance.end_time or room != instance.room or day != instance.day:
                    overlapping_meetings = Meeting.objects.filter(
                        room=room,
                        day=day,
                        start_time__lt=end_time,
                        end_time__gt=start_time
                    ).exclude(id=instance.id)  # Exclude the current instance to avoid self-conflict

                    if overlapping_meetings.exists():
                        raise serializers.ValidationError("This meeting overlaps with an existing meeting.")
                else:
                    overlapping_meetings = Meeting.objects.filter(
                        room=room,
                        day=day,
                        start_time__lt=end_time,
                        end_time__gt=start_time
                    ) 

                    if overlapping_meetings.exists():
                        raise serializers.ValidationError("This meeting overlaps with an existing meeting.")
            else:  # During creation
                overlapping_meetings = Meeting.objects.filter(
                    room=room,
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