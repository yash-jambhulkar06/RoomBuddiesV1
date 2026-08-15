from django.urls import path
from .import views

app_name="reviews"

urlpatterns=[
   path("<int:booking_id>/add/",views.add_review,name="add_review"),
   path("service/<int:booking_id>/review/",views.add_service_review,name="add_service_review"),
]