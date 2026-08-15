from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.user_services.models import ServiceBooking
from apps.bookings.models import Booking

from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
    )

    if booking.status != Booking.Status.ACCEPTED:
        messages.error(
            request,
            "You can review only accepted bookings.",
        )
        return redirect("bookings:my_bookings")

    if Review.objects.filter(booking=booking).exists():
        messages.warning(
            request,
            "You have already reviewed this booking.",
        )
        return redirect("bookings:my_bookings")

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)
            review.room = booking.room
            review.user = request.user
            review.booking = booking
            review.save()

            messages.success(
                request,
                "Review submitted successfully.",
            )

            return redirect("bookings:my_bookings")

    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "booking": booking,
        },
    )



@login_required
def add_service_review(request, booking_id):

    service_booking = get_object_or_404(
        ServiceBooking,
        id=booking_id,
        user=request.user,
    )

    if service_booking.status != ServiceBooking.Status.COMPLETED:
        messages.error(
            request,
            "You can review only completed services.",
        )
        return redirect("user_services:my_service_bookings")

    if Review.objects.filter(
        service_booking=service_booking
    ).exists():

        messages.warning(
            request,
            "You have already reviewed this service.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.user = request.user
            review.service_booking = service_booking

            review.save()

            messages.success(
                request,
                "Service review submitted successfully.",
            )

            return redirect(
                "user_services:my_service_bookings"
            )

    else:

        form = ReviewForm()

    return render(
        request,
        "reviews/add_service_review.html",
        {
            "form": form,
            "service_booking": service_booking,
        },
    )