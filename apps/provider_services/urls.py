from django.urls import path
from . import views

app_name = "provider_services"

urlpatterns = [
    path(
        "add/",
        views.add_service,
        name="add_service",
    ),
    
    
    path("my/",views.my_services,name="my_services"),
    
    path("edit/<int:service_id>/",views.edit_service,name="edit_service"),
    path("delete/<int:service_id>/",views.delete_service,name="delete_service"),
    path("booking-requests/",views.service_booking_requests,name="service_booking_requests"),
    path(
    "service-bookings/<int:booking_id>/<str:status>/",
    views.update_service_booking_status,
    name="update_service_booking_status",
    ),
    
    path(
    "service-requests/<int:booking_id>/complete/",
    views.complete_service_booking,
    name="complete_service_booking",
    ),
    
    
    path("payments/",views.provider_payments,name="provider_payments"),
]