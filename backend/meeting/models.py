from django.db import models
from django.contrib.auth.models import User
from room.models import Room
class Meeting(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="meetings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meetings")
    extra_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
