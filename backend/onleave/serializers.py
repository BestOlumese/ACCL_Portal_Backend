from rest_framework import serializers
from .models import Leave
    
class LeaveSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    director_name = serializers.CharField(source='director.username', read_only=True)

    class Meta:
        model = Leave
        fields = ["id","content", "start_date", "end_date", "username", "director", "director_name", "status", "created_at"]
        extra_kwargs = {"username": {"read_only": True}, "status": {"read_only": True}}

class LeaveAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ["status"]