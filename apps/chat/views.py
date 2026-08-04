from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.rooms.models import Room
from .models import Conversation
from django.http import HttpResponseForbidden
from .forms import MessageForm

from django.db.models import Q


@login_required
def conversation_list(request):
    conversations = (
        Conversation.objects.filter(
            Q(user=request.user) |
            Q(provider=request.user)
        )
        .select_related(
            "room",
            "user",
            "provider",
        )
        .order_by("-created_at")
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

    messages = conversation.messages.select_related(
        "sender"
    ).all()

    return render(
        request,
        "chat/chat_room.html",
        {
            "conversation": conversation,
            "messages": messages,
            "form": form,
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
    
