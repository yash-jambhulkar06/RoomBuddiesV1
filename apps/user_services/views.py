from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.provider_services.models import Service
from django.contrib import messages
from .forms import ServiceBookingForm
from .models import ServiceBooking
from apps.services.notification_service import create_notification
from apps.services.payment_service import create_service_payment_order,verify_payment,Payment
from apps.reviews.models import Review
from django.db.models import Avg

@login_required
def service_list(request):
    services=Service.objects.filter(
        is_available=True
    ).select_related(
        "provider"
    )
    
    return render(
        request,
        "user_services/service_list.html",
        {
            "services":services
        }
    )
    
    



@login_required
def service_details(request,service_id):
    service=get_object_or_404(
        Service,
        id=service_id,
        is_available=True,
    )
    
    reviews=Review.objects.filter(
        service_booking__service=service
    ).select_related(
        "user",
        "service_booking",
    )
    
    average_rating=reviews.aggregate(
        average=Avg("rating")
    )["average"]
    
    return render(
        request,
        "user_services/service_detail.html",
        {
            "service":service,
            "reviews":reviews,
            "average_rating":average_rating,
        }
    )
    
    
    
@login_required
def book_service(request, service_id):

    service = get_object_or_404(
        Service,
        id=service_id,
        is_available=True,
    )

    if request.method == "POST":

        form = ServiceBookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.user = request.user
            booking.service = service
            booking.status = ServiceBooking.Status.PENDING

            booking.save()
            create_notification(
                user=service.provider,
                title="New Service Booking",
                message=(
                    f"{request.user.first_name}"
                    f"{request.user.last_name} requested"
                    f"your service :{service.title}."
                ),
                notification_type="SERVICE_BOOKING",
            )

            messages.success(
                request,
                "Service booking request submitted successfully.",
            )

            return redirect(
                "user_services:service_list"
            )

    else:

        form = ServiceBookingForm()

    return render(
        request,
        "user_services/book_service.html",
        {
            "form": form,
            "service": service,
        },
    )
    
    

@login_required
def my_service_booking(request):
    bookings=ServiceBooking.objects.filter(
        user=request.user,
        
    ).select_related(
        "service",
        "service__provider",
    )
    
    return render(
        request,
        "user_services/my_service_bookings.html",
        {
            "bookings":bookings,
        }
    )
    
    
    


@login_required
def cancel_service_booking(request, booking_id):

    booking = get_object_or_404(
        ServiceBooking.objects.select_related(
            "service",
            "service__provider",
        ),
        
        id=booking_id,
        user=request.user,
        
    )

    if request.method != "POST":
        return redirect(
            "user_services:my_service_bookings"
        )

    if booking.status not in [
        ServiceBooking.Status.PENDING,
        ServiceBooking.Status.ACCEPTED,
    ]:
        messages.error(
            request,
            "This booking cannot be cancelled.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )
        
    payment=getattr(
            booking,
            "payment",
            None,
        )
        
    if(
            payment and payment.status == Payment.Status.SUCCESS
        ):
            messages.error(request,"This booking cannot be cancelled.")
            
            return redirect("user_services:my_service_bookings")

    booking.status = ServiceBooking.Status.CANCELLED

    booking.save(
    update_fields=["status"]
    )

    create_notification(
        user=booking.service.provider,
    title="Service Booking Cancelled",
    message=(
        f"{request.user.first_name} "
        f"{request.user.last_name} cancelled "
        f"the booking for your service: "
        f"{booking.service.title}."
    ),
    notification_type="SERVICE_BOOKING_CANCELLED",
    )

    messages.success(
        request,
        "Service booking cancelled successfully.",
    )

    return redirect(
        "user_services:my_service_bookings"
    )
    
    

@login_required
def service_payment(request, booking_id):

    booking = get_object_or_404(
        ServiceBooking.objects.select_related(
            "service",
            "service__provider",
        ),
        id=booking_id,
        user=request.user,
    )

    if booking.status != ServiceBooking.Status.ACCEPTED:
        messages.error(
            request,
            "Payment is available only after the provider accepts your booking.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    if hasattr(booking, "payment") and booking.payment.status == "SUCCESS":
        messages.info(
            request,
            "This booking has already been paid.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    payment, order = create_service_payment_order(
        booking
    )

    return render(
        request,
        "user_services/service_payment.html",
        {
            "booking": booking,
            "payment": payment,
            "order": order,
        },
    )
    
    

@login_required
def verify_service_payment(request, booking_id):

    booking = get_object_or_404(
        ServiceBooking.objects.select_related(
            "service",
            "service__provider",
        ),
        id=booking_id,
        user=request.user,
    )

    if request.method != "GET":
        return redirect(
            "user_services:my_service_bookings"
        )

    # Payment record must exist
    payment = getattr(booking, "payment", None)

    if payment is None:
        messages.error(
            request,
            "Payment record was not found.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    # Prevent verifying an already successful payment
    if payment.status == Payment.Status.SUCCESS:
        messages.info(
            request,
            "This payment has already been completed.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    razorpay_payment_id = request.GET.get(
        "razorpay_payment_id"
    )

    razorpay_order_id = request.GET.get(
        "razorpay_order_id"
    )

    razorpay_signature = request.GET.get(
        "razorpay_signature"
    )

    # Make sure Razorpay returned all required values
    if not all(
        [
            razorpay_payment_id,
            razorpay_order_id,
            razorpay_signature,
        ]
    ):

        messages.error(
            request,
            "Incomplete payment information received.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    # Verify payment
    try:

        verify_payment(
            payment=payment,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_order_id=razorpay_order_id,
            razorpay_signature=razorpay_signature,
        )

    except Exception:
        messages.error(
            request,
            "Payment verification failed.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    # Payment was successfully verified
    create_notification(
        user=booking.user,
        title="Payment Successful",
        message=(
            f"Payment of ₹{payment.amount} for "
            f"{booking.service.title} was successful."
        ),
        notification_type="SERVICE_PAYMENT_SUCCESS",
    )

    create_notification(
        user=booking.service.provider,
        title="Payment Received",
        message=(
            f"Payment of ₹{payment.amount} received for "
            f"{booking.service.title}."
        ),
        notification_type="SERVICE_PAYMENT_RECEIVED",
    )

    messages.success(
        request,
        "Payment completed successfully.",
    )

    return redirect(
        "user_services:my_service_bookings"
    )
    

@login_required
def review_service(request, booking_id):

    booking = get_object_or_404(
        ServiceBooking.objects.select_related(
            "service",
            "service__provider",
        ),
        id=booking_id,
        user=request.user,
    )

    # Only completed bookings can be reviewed
    if booking.status != ServiceBooking.Status.COMPLETED:
        messages.error(
            request,
            "You can review a service only after it is completed.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    # Prevent duplicate reviews
    if hasattr(booking, "review"):
        messages.info(
            request,
            "You have already reviewed this service.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()

        if not rating or not comment:
            messages.error(
                request,
                "Rating and comment are required.",
            )

            return render(
                request,
                "user_services/review_service.html",
                {"booking": booking},
            )

        try:
            rating = int(rating)
        except (TypeError, ValueError):

            messages.error(
                request,
                "Invalid rating.",
            )

            return render(
                request,
                "user_services/review_service.html",
                {"booking": booking},
            )

        if rating < 1 or rating > 5:

            messages.error(
                request,
                "Rating must be between 1 and 5.",
            )

            return render(
                request,
                "user_services/review_service.html",
                {"booking": booking},
            )

        from apps.reviews.models import Review

        Review.objects.create(
            service_booking=booking,
            user=request.user,
            rating=rating,
            comment=comment,
        )

        messages.success(
            request,
            "Thank you! Your review has been submitted.",
        )

        return redirect(
            "user_services:my_service_bookings"
        )

    return render(
        request,
        "user_services/review_service.html",
        {"booking": booking},
    )