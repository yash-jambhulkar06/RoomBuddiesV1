from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth import get_user_model
from .models import Conversation,Message


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.conversation_id=self.scope["url_route"]["kwargs"]["conversation_id"]
        
        self.room_group_name=f"chat_{self.conversation_id}"
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        data=json.loads(text_data)
        if data["type"] =="typing":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,{
                    "type":"typing_status",
                    "sender_id":self.scope["user"].id,
                },
            )
            return
        user=self.scope["user"]
        conversation=Conversation.objects.get(
            id=self.conversation_id
        )
        
        message=Message.objects.create(
            conversation=conversation,
            sender=user,
            message=data["message"],
        )
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                "type":"chat_message",
                "message":message.message,
                "sender":user.first_name,
                "sender_id":user.id,
                "time":message.created_at.strftime("%d %b %H: %M"),
            }
        )
        
    def chat_message(self,event):
        message=event["message"],
        
        self.send(
            text_data=json.dumps({
                "type":"message",
                "message":event["message"],
                "sender":event["sender"],
                "sender_id":event["sender_id"],
                "time":event["time"],
            })
        )
        
    def typing_status(self,event):
        self.send(
            text_data=json.dumps({
                "type":"typing",
                "sender_id":event["sender_id"],
            })
        )