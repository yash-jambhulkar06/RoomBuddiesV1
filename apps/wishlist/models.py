from django.db import models
from django.conf import settings
from apps.rooms.models import Room


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "room"],
                name="unique_user_room_wishlist",
            )
        ]

    def __str__(self):
        return f"{self.user.email} ❤️ {self.room.title}"