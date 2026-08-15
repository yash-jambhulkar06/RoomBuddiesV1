import razorpay
from django.conf import settings

from apps.payments.models import Payment


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)


def create_payment_order(booking):
    """
    Create Razorpay Order
    """

    payment = Payment.objects.create(
        booking=booking,
        user=booking.user,
        provider=booking.room.owner,
        amount=booking.room.rent,
    )
    
    print("Room Rent=",booking.room.rent)
    print("Payment Amount=",payment.amount)
    print("Amount sent to Razorpay =",int(payment.amount*100))

    order = client.order.create(
        {
            "amount": int(payment.amount * 100),
            "currency": "INR",
            "payment_capture": 1,
        }
    )

    payment.razorpay_order_id = order["id"]
    payment.save()

    return payment, order


def verify_payment(
    *,
    payment,
    razorpay_payment_id,
    razorpay_order_id,
    razorpay_signature,
):

    if payment.razorpay_order_id != razorpay_order_id:
        raise ValueError(
            "Razorpay order does not match the payment record."
        )

    client.utility.verify_payment_signature(
        {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }
    )

    payment.status = Payment.Status.SUCCESS

    payment.razorpay_payment_id = razorpay_payment_id

    payment.razorpay_signature = razorpay_signature

    payment.save(
        update_fields=[
            "status",
            "razorpay_payment_id",
            "razorpay_signature",
        ]
    )

    return payment


def create_service_payment_order(service_booking):

    payment = Payment.objects.filter(
        service_booking=service_booking,
        status=Payment.Status.PENDING,
    ).first()

    if payment is None:

        payment = Payment.objects.create(
            service_booking=service_booking,
            user=service_booking.user,
            provider=service_booking.service.provider,
            amount=service_booking.service.price,
        )

    # Reuse the existing Razorpay order if one already exists
    if payment.razorpay_order_id:

        order = client.order.fetch(
            payment.razorpay_order_id
        )

    else:

        order = client.order.create(
            {
                "amount": int(payment.amount * 100),
                "currency": "INR",
                "payment_capture": 1,
            }
        )

        payment.razorpay_order_id = order["id"]

        payment.save(
            update_fields=["razorpay_order_id"]
        )

    return payment, order