from django.db import models
from django.conf import settings
from apps.rooms.models import Room

class Booking(models.Model):
    
    class Status(models.TextChoices):
        PENDING="PENDING","Pending"
        ACCEPTED="ACCEPTED","Accepted"
        REJECTED="REJECTED","Rejected"
        
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
        
    room=models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
        
    status=models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
        
    created_at=models.DateTimeField(
        auto_now_add=True,
    )
        
    def __str__(self):
        return f"{self.user.email}{self.room.title}"