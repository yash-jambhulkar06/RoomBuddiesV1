from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.decorators import login_required

from apps.rooms.models import Room
from apps.bookings.models import Booking

from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    booked = Booking.objects.filter(
        user=request.user,
        room=room,
        status=Booking.Status.ACCEPTED,
    ).exists()

    if not booked:
        return redirect("rooms:room_detail", id=room.id)

    if Review.objects.filter(
        user=request.user,
        room=room,
    ).exists():
        return redirect("rooms:room_detail", id=room.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room = room
            review.save()

            return redirect("rooms:room_detail", id=room.id)

    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "room": room,
        },
    )
    

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )

    if request.method == "POST":
        form = ReviewForm(
            request.POST,
            instance=review,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "rooms:room_detail",
                id=review.room.id,
            )

    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/edit_review.html",
        {
            "form": form,
            "room": review.room,
        },
    )
    
    


@login_required
def delete_review(request,review_id):
    review=get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )
    
    room_id=review.room.id
    review.delete()
    
    return redirect(
        "rooms:room_detail",
        id=room_id,
    )