from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from .models import Service
from .forms import ServiceForm
from apps.user_services.models import ServiceBooking
from apps.services.notification_service import create_notification
from apps.payments.models import Payment
from django.db.models import Sum

@login_required
def add_service(request):

    if request.method == "POST":

        form = ServiceForm(request.POST)

        if form.is_valid():

            service = form.save(commit=False)
            service.provider = request.user
            service.save()

            messages.success(
                request,
                "Service added successfully.",
            )

            return redirect("provider_services:my_services")

    else:
        form = ServiceForm()

    return render(
        request,
        "provider_services/add_service.html",
        {
            "form": form,
        },
    )
    
    

@login_required
def my_services(request):
    services=Service.objects.filter(
        provider=request.user
    )
    
    return render(request,"provider_services/my_services.html",{"services":services})


@login_required
def edit_service(request,service_id):
    service=get_object_or_404(
        Service,
        id=service_id,
        provider=request.user,
    )
    
    if request.method == "POST":
        form =ServiceForm(
            request.POST,
            instance=service,
        )
        
        if form.is_valid():
            form.save()
            
            messages.success(request,"Service updated successfully.")
            
            return redirect("provider_services:my_services")
        
    else:
            form= ServiceForm(
                instance=service
            )
            
    return render(request,"provider_services/edit_service.html",{ "form":form, "service":service })



@login_required
def delete_service(request,service_id):
    service=get_object_or_404(
        Service,
        id=service_id,
        provider=request.user
    )
    
    if request.method == 'POST':
        service.delete()
        
        messages.success(request,"Services deleted successfully.")
        
        return redirect("provider_services:my_services")
    
    return render(request,"provider_services/delete_service.html",{ "service":service, })




@login_required
def service_booking_requests(request):

    bookings = ServiceBooking.objects.filter(
        service__provider=request.user
    ).select_related(
        "user",
        "service",
    )

    return render(
        request,
        "provider_services/service_booking_requests.html",
        {
            "bookings": bookings,
        },
    )
    
    


@login_required
def update_service_booking_status(request, booking_id, status):

    booking = get_object_or_404(
        ServiceBooking,
        id=booking_id,
        service__provider=request.user,
    )

    if request.method != "POST":
        return redirect(
            "provider_services:service_booking_requests"
        )

    # Only pending bookings can be accepted or rejected
    if booking.status != ServiceBooking.Status.PENDING:
        messages.error(
            request,
            "This booking has already been processed.",
        )

        return redirect(
            "provider_services:service_booking_requests"
        )

    if status == ServiceBooking.Status.ACCEPTED:

        booking.status = ServiceBooking.Status.ACCEPTED

        booking.save(
            update_fields=["status"]
        )

        create_notification(
            user=booking.user,
            title="Service Booking Accepted",
            message=(
                f"Your booking for "
                f"{booking.service.title} "
                f"has been accepted by the provider."
            ),
            notification_type="SERVICE_BOOKING_ACCEPTED",
        )

        messages.success(
            request,
            f"Booking #{booking.id} accepted.",
        )

    elif status == ServiceBooking.Status.REJECTED:

        booking.status = ServiceBooking.Status.REJECTED

        booking.save(
            update_fields=["status"]
        )

        create_notification(
            user=booking.user,
            title="Service Booking Rejected",
            message=(
                f"Your booking for "
                f"{booking.service.title} "
                f"has been rejected by the provider."
            ),
            notification_type="SERVICE_BOOKING_REJECTED",
        )

        messages.success(
            request,
            f"Booking #{booking.id} rejected.",
        )

    else:

        messages.error(
            request,
            "Invalid booking status.",
        )

    return redirect(
        "provider_services:service_booking_requests"
    )
    
    

@login_required
def complete_service_booking(request, booking_id):
    print(">>>COMPLETE_SERVICE_BOOKING VIEW CALLED",booking_id,)

    booking = get_object_or_404(
        ServiceBooking.objects.select_related(
            "service",
            "service__provider",
            "user",
        ),
        id=booking_id,
        service__provider=request.user,
    )

    # Only POST requests are allowed
    if request.method != "POST":
        return redirect(
            "provider_services:service_booking_requests"
        )

    # Only accepted bookings can be completed
    if booking.status != ServiceBooking.Status.ACCEPTED:
        messages.error(
            request,
            "Only accepted bookings can be completed.",
        )

        return redirect(
            "provider_services:service_booking_requests"
        )

    # Get payment belonging to THIS booking
    payment = getattr(
        booking,
        "payment",
        None,
    )

    # Payment must exist
    if payment is None:
        messages.error(
            request,
            "This booking has not been paid yet.",
        )

        return redirect(
            "provider_services:service_booking_requests"
        )

    # Make sure payment belongs to this exact booking
    if payment.service_booking_id != booking.id:
        messages.error(
            request,
            "Invalid payment record for this booking.",
        )

        return redirect(
            "provider_services:service_booking_requests"
        )

    # Payment must be successful
    if payment.status != Payment.Status.SUCCESS:
        messages.error(
            request,
            "Payment must be completed before completing the service.",
        )

        return redirect(
            "provider_services:service_booking_requests"
        )

    # Complete the booking
    booking.status = ServiceBooking.Status.COMPLETED

    booking.save(
        update_fields=["status"]
    )

    # Notify customer
    create_notification(
        user=booking.user,
        title="Service Completed",
        message=(
            f"Your service booking for "
            f"{booking.service.title} "
            f"has been completed."
        ),
        notification_type="SERVICE_COMPLETED",
    )

    messages.success(
        request,
        f"Booking #{booking.id} marked as completed.",
    )

    return redirect(
        "provider_services:service_booking_requests"
    )
    
    
    


@login_required
def provider_payments(request):

    payments = (
        Payment.objects
        .filter(
            provider=request.user,
            status=Payment.Status.SUCCESS,
        )
        .select_related(
            "user",
            "booking",
            "service_booking",
            "service_booking__service",
        )
        .order_by("-created_at")
    )

    total_earnings = payments.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "provider_services/payments.html",
        {
            "payments": payments,
            "total_earnings": total_earnings,
        },
    )
    
    
    