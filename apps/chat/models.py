from django.conf import settings
from django.db import models

from apps.rooms.models import Room


class Conversation(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="conversations",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_conversations",
    )

    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_conversations",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "room",
            "user",
            "provider",
        )

    def __str__(self):
        return f"{self.user.email} → {self.provider.email} ({self.room.title})"