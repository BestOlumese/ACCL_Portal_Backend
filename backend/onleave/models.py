from django.db import models
from django.contrib.auth.models import User

class Leave(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        DISAPPROVED = 'disapproved', 'Disapproved'

    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaves")
    director = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="director")
    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.PENDING 
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
