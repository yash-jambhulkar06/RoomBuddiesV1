from django.urls import path
from .import views

app_name="user_services"

urlpatterns=[
    path("",views.service_list,name="service_list"),
    path("<int:service_id>/",views.service_details,name="service_details"),
    path("<int:service_id>/book/",views.book_service,name="book_service"),
    path("my-bookings/",views.my_service_booking,name="my_service_bookings"),
    path(
    "my-bookings/<int:booking_id>/cancel/",
    views.cancel_service_booking,
    name="cancel_service_booking",
    ),
    
    path("my-bookings/<int:booking_id>/payment/",views.service_payment,name="service_payment"),
    path("my-bookings/<int:booking_id>/payment/verify/",views.verify_service_payment,name="verify_service_payment"),
    path("my-bookings/<int:booking_id>/review/",views.review_service,name="review_service"),
]