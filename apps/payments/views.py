from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from apps.payments.models import Payment
from apps.bookings.models import Booking
from apps.services.payment_service import create_payment_order,verify_payment
from django.conf import settings

@login_required
def create_payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
    )

    payment, order = create_payment_order(
        booking
    )

    context = {
        "payment": payment,
        "order": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    }

    return render(
        request,
        "payments/payment_page.html",
        context,
    )
    
@login_required
def verify_payment_view(request):

    payment_id = request.GET.get("payment_id")
    order_id = request.GET.get("order_id")
    signature = request.GET.get("signature")

    payment = Payment.objects.get(
        razorpay_order_id=order_id
    )

    verify_payment(
        payment=payment,
        razorpay_payment_id=payment_id,
        razorpay_order_id=order_id,
        razorpay_signature=signature,
       
    )
    
    payment.booking.status = Booking.Status.ACCEPTED
    payment.booking.save()

    return redirect("bookings:my_bookings")

