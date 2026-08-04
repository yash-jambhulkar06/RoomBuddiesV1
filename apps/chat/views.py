from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.rooms.models import Room
from .models import Conversation

@login_required
def conversation_list(request):
    return render(request,"chat/conversation_list.html")

@login_required
def chat_room(request):
    return render(request,"chat/chat_room.html")

@login_required
def start_conversation(request,room_id):
    room=get_object_or_404(Room,id=room_id)
    conversation, created= Conversation.objects.get_or_create(
                room=room,
                user=request.user,
                provider=room.owner,
            )
        
    return redirect("chat:chat_room",conversation_id=conversation.id,)
    
