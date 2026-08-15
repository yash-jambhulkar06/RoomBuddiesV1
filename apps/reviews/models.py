from django.db import models
from django.conf import settings

from apps.rooms.models import Room
from apps.bookings.models import Booking
from apps.user_services.models import ServiceBooking


class Review(models.Model):

    class Rating(models.IntegerChoices):
        ONE = 1, "1 Star"
        TWO = 2, "2 Stars"
        THREE = 3, "3 Stars"
        FOUR = 4, "4 Stars"
        FIVE = 5, "5 Stars"

    # For room reviews
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True,
    )

    # For room bookings
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="review",
        null=True,
        blank=True,
    )

    # For service reviews
    service_booking = models.OneToOneField(
        ServiceBooking,
        on_delete=models.CASCADE,
        related_name="review",
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        choices=Rating.choices,
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):

        if self.room:
            return f"{self.room.title} - {self.rating}★"

        if self.service_booking:
            return (
                f"{self.service_booking.service.title} "
                f"- {self.rating}★"
            )

        return f"Review #{self.id} - {self.rating}★"