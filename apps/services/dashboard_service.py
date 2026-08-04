from django.db.models import Count, Avg

from apps.rooms.models import Room
from apps.bookings.models import Booking
from apps.reviews.models import Review


def get_provider_dashboard_data(user):
    rooms = (
        Room.objects.filter(owner=user)
        .annotate(booking_count=Count("bookings"))
    )

    total_rooms = rooms.count()

    total_bookings = Booking.objects.filter(
        room__owner=user
    ).count()

    pending_requests = Booking.objects.filter(
        room__owner=user,
        status=Booking.Status.PENDING,
    ).count()

    average_rating = Review.objects.filter(
        room__owner=user
    ).aggregate(
        Avg("rating")
    )["rating__avg"]

    recent_bookings = (
        Booking.objects.filter(room__owner=user)
        .select_related("user", "room")
        .order_by("-created_at")[:5]
    )

    recent_reviews = (
        Review.objects.filter(room__owner=user)
        .select_related("user", "room")
        .order_by("-created_at")[:5]
    )

    return {
        "stats": {
            "total_rooms": total_rooms,
            "total_bookings": total_bookings,
            "pending_requests": pending_requests,
            "average_rating": average_rating,
        },
        "rooms": rooms,
        "recent_bookings": recent_bookings,
        "recent_reviews": recent_reviews,
    }