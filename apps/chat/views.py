from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.rooms.models import Room
from .models import Conversation
from django.http import HttpResponseForbidden
from .forms import MessageForm
from .services import mark_conversation_as_read
from .selector import get_user_conversations

from django.db.models import Q


@login_required
def conversation_list(request):
    conversations=get_user_conversations(
        request.user
    )
    return render(
        request,
        "chat/conversation_list.html",
        {
            "conversations": conversations,
        },
    )

@login_required
def chat_room(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
    )

    if request.user not in (
        conversation.user,
        conversation.provider,
    ):
        return HttpResponseForbidden(
            "You are not allowed to access this conversation."
        )

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()

            return redirect(
                "chat:chat_room",
                conversation_id=conversation.id,
            )

    else:
        form = MessageForm()

    mark_conversation_as_read(
        conversation,
        request.user,
    )
    
    messages=conversation.messages.select_related(
        "sender"
    ).all()
    
    print("Logged in user:", request.user.email)
    print("Conversation user:", conversation.user.email)
    print("Conversation provider:", conversation.provider.email)

    if request.user == conversation.user:
        other_user = conversation.provider
    else:
        other_user = conversation.user

    print("Other user:", other_user.email)

    return render(
        request,
        "chat/chat_room.html",
        {
            "conversation": conversation,
            "messages": messages,
            "form": form,
            "other_user":other_user,
        },
    )

@login_required
def start_conversation(request,room_id):
    room=get_object_or_404(Room,id=room_id)
    conversation, created= Conversation.objects.get_or_create(
                room=room,
                user=request.user,
                provider=room.owner,
            )
        
    return redirect("chat:chat_room",conversation_id=conversation.id,)
    
