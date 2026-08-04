from django.urls import path
from .views import create_room,room_detail,room_list,edit_room,delete_room

app_name="rooms"

urlpatterns=[
    path("create/",create_room,name="create_room"),
    path("<int:id>/",room_detail,name="room_detail"),
    path("",room_list,name="room_list"),
    path("<int:id>/edit/",edit_room,name="edit_room"),
    path("<int:id>/delete/",delete_room,name="delete_room")
]