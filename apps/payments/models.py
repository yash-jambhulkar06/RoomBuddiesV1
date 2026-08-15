from django.db import models
from django.conf import settings

from apps.bookings.models import Booking
from apps.user_services.models import ServiceBooking


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment",
        null=True,
        blank=True,
    )
    
    service_booking=models.OneToOneField(
        ServiceBooking,
        on_delete=models.CASCADE,
        related_name="payment",
        null=True,
        blank=True
        
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    razorpay_order_id = models.CharField(
        max_length=200,
        blank=True,
    )

    razorpay_payment_id = models.CharField(
        max_length=200,
        blank=True,
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        if self.booking:
            return f"Room Booking #{self.booking.id} - {self.status}"
        
        if self.service_booking:
            return f"Service Booking #{self.service_booking.id} - {self.status}"
        
        return f"Payment #{self.id} - {self.status}"
    
    
    

