from rest_framework import serializers
from .models import Leave
    
class LeaveSerializer(serializers.ModelSerializer):
    user_firstname = serializers.CharField(source='user.first_name', read_only=True)
    user_lastname = serializers.CharField(source='user.last_name', read_only=True)
    user_total_leaves = serializers.CharField(source='user.userprofile.total_leaves', read_only=True)
    user_leaves_balance = serializers.CharField(source='user.userprofile.leaves', read_only=True)
    user_name = serializers.SerializerMethodField()  # Combined user name field

    director_firstname = serializers.CharField(source='director.first_name', read_only=True)
    director_lastname = serializers.CharField(source='director.last_name', read_only=True)
    director_name = serializers.SerializerMethodField()  # Combined director name field

    class Meta:
        model = Leave
        fields = ["id", "content", "start_date", "end_date", "user", "user_firstname", "user_lastname", "user_name", "user_total_leaves", "user_leaves_balance", "director", "director_firstname", "director_lastname", "director_name", "status", "created_at"]
        extra_kwargs = {"user": {"read_only": True}, "status": {"read_only": True}}

    def get_user_name(self, obj):
        # Combine the first and last name for the user
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_director_name(self, obj):
        # Combine the first and last name for the director
        return f"{obj.director.first_name} {obj.director.last_name}"

class LeaveAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ["status"]