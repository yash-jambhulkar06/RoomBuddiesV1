from django.db import models
from django.conf import settings


class Service(models.Model):

    class ServiceType(models.TextChoices):
        TIFFIN = "TIFFIN", "Tiffin"
        LAUNDRY = "LAUNDRY", "Laundry"
        WATER_CAN = "WATER_CAN", "Water Can"

    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_services",
    )

    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
    )

    title = models.CharField(
        max_length=150,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    is_available = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.service_type})"