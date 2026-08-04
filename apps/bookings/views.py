from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect,render
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib import  messages
from apps.rooms.models import Room
from .models import Booking

@login_required
def book_room(request,room_id):
    room=get_object_or_404(Room,id=room_id)
    
    if room.owner==request.user:
       
        messages.error(request,"You cannot book your own room.")
        return redirect("rooms:room_detail",room.id)
    
    
    if Booking.objects.filter(
        user=request.user,
        room=room,
        status=Booking.Status.PENDING,
    ).exists():
        messages.warning(
            request,"You have already requested this room",
        )
        
        return redirect("rooms:room_detail",room.id)
    
    Booking.objects.create(
        user=request.user,
        room=room,
    )
    
    messages.success(request,"Booking request sent successfully!",)
    return redirect("bookings:my_bookings")

@login_required
def owner_bookings(request):
    bookings=Booking.objects.filter(
        room__owner=request.user
    ).order_by("-created_at")
    
    
    return render(request,"bookings/owner_bookings.html",{"bookings":bookings,},)




@login_required
def accept_booking(request,booking_id):
    booking=get_object_or_404(
        Booking,
        id=booking_id,
    )
    
    if booking.room.owner!=request.user:
        return HttpResponseForbidden(
            "You are not allowed to accept this booking."
        )
        
        
    booking.status=Booking.Status.ACCEPTED
    booking.save()
    
    return redirect("bookings:owner_bookings")


@login_required
def reject_booking(request,booking_id):
    booking=get_object_or_404(
        Booking,
        id=booking_id,
    )
    
    if booking.room.owner!=request.user:
        return HttpResponseForbidden("You are not allowed to reject this booking.")
    
    booking.status=Booking.Status.REJECTED
    booking.save()
    
    return("bookings:owner_bookings")



@login_required
def my_bookings(request):
    bookings=Booking.objects.filter(
        user=request.user
    ).order_by("-created_at")
    
    return render(request,"bookings/my_bookings.html",{"bookings":bookings,},)