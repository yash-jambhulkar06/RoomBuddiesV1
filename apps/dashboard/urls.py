from django.urls import path
from .views import provider_dashboard

app_name="dashboard"

urlpatterns=[
    path("provider/",provider_dashboard,name="provider_dashboard"),
]