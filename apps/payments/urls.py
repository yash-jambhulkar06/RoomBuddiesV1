from django.urls import path
from .views import create_payment,verify_payment_view

app_name="payments"

urlpatterns=[
    path("<int:booking_id>/",create_payment,name="create_payment"),
    path("verify/",verify_payment_view,name="verify_payment"),
]