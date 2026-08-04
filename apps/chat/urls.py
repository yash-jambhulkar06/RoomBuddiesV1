from django.urls import path
from .import views

app_name="chat"

urlpatterns=[
    path("",views.conversation_list,name="conversation_list"),
    path("start/<int:room_id>/",views.start_conversation,name="start_conversation"),
    path("<int:conversation_id>/",views.chat_room,name="chat_room"),
]