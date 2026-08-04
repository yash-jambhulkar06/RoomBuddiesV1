from django.urls import path
from .views import toggle_wishlist,wishlist_list

app_name="wishlist"

urlpatterns=[
    path("toggle/<int:room_id>/",toggle_wishlist,name="toggle_wishlist"),
    path("",wishlist_list,name="wishlist_list"),
]