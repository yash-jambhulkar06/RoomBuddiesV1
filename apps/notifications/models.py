from django.conf import settings
from django.db import models


class Notification(models.Model):

    class Type(models.TextChoices):

        BOOKING = "BOOKING", "Booking"

        SERVICE_BOOKING_ACCEPTED = (
        "SERVICE_BOOKING_ACCEPTED",
        "Service Booking Accepted",
        )

        SERVICE_BOOKING_REJECTED = (
            "SERVICE_BOOKING_REJECTED",
            "Service Booking Rejected",
        )

        SERVICE_BOOKING_CANCELLED = (
            "SERVICE_BOOKING_CANCELLED",
            "Service Booking Cancelled",
        )

        SERVICE_COMPLETED = (
            "SERVICE_COMPLETED",
            "Service Completed",
        )

        PAYMENT_RECEIVED = (
            "PAYMENT_RECEIVED",
            "Payment Received",
        )

        PAYMENT_SUCCESS = (
            "PAYMENT_SUCCESS",
            "Payment Successful",
        )

        MESSAGE = "MESSAGE", "Message"

        REVIEW = "REVIEW", "Review"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    type = models.CharField(
        max_length=50,
        choices=Type.choices,
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title