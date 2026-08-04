from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count,Avg
from apps.rooms.models import Room
from apps.bookings.models import Booking
from apps.reviews.models import Review
from apps.common.decorators import provider_required

@login_required
@provider_required
def provider_dashboard(request):
    rooms=Room.objects.filter(
        owner=request.user
    ).annotate(
        booking_count=Count("bookings")
    )
    
    total_rooms=rooms.count()
    
    total_bookings=Booking.objects.filter(
        room__owner=request.user,
    ).count()
    
    pending_requests=Booking.objects.filter(
        room__owner=request.user,
        status=Booking.Status.PENDING,
    ).count()
    
    average_rating=Review.objects.filter(
        room__owner=request.user
    ).aggregate(
        Avg("rating")
    )["rating_avg"]
    
    
    recent_bookings=Booking.objects.filter(
        room__owner=request.user
    ).select_related(
        "user",
        "room",
    ).order_by("-created_at")[:5]
    
    recent_reviews=Review.objects.filter(
        room__owner=request.user
    ).select_related(
        "user",
        "room",
    ).order_by("-created_at")[:5]
    
    context={
        "stats":{
        "rooms":rooms,
        "total_rooms":total_rooms,
        "total_bookings":total_bookings,
        "pending_requests":pending_requests,
        "average_rating":average_rating,
        },
        "rooms":rooms,
        "recent_bookings":recent_bookings,
        "recent_reviews":recent_reviews,
    }
    
    
    return render(request,
                  "dashboard/provider_dashboard.html",
                  context,)
    
    

