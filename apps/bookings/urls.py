from django.urls import path
from .views import (
    book_room,
    owner_bookings,
    accept_booking,
    reject_booking,
    my_bookings,
)

app_name="bookings"

urlpatterns=[
    path("<int:room_id>/book/",book_room,name="book_room"),
    path("owner/",owner_bookings,name="owner_bookings"),
    path("<int:booking_id>/accept/",accept_booking,name="accept_booking"),
    path("<int:booking_id>/reject/",reject_booking,name="reject_booking"),
    path("my/",my_bookings,name="my_bookings"),

]