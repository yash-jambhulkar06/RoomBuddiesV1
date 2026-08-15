from django.conf import settings

def razorpay_settings(request):
    return{
        "RAZORPAY_KEY_ID":settings.RAZORPAY_KEY_ID,
    }