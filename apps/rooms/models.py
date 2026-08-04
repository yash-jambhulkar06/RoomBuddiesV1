from django.db import models
from django.conf import settings

class Room(models.Model):
    owner=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        )
    
    
    title=models.CharField(max_length=200)
    description=models.TextField()
    rent=models.DecimalField(max_digits=10,decimal_places=2)
    location=models.CharField(max_length=255)
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    
    image=models.ImageField(
        upload_to="rooms/",
        blank=True,
        null=True,
    )
    
    
    
    def __str__(self):
        return self.title


