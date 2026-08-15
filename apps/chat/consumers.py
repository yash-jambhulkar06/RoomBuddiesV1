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
        self.scope["user"].is_online = True
        self.scope["user"].save(update_fields=["is_online"])
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                "type":"user_status",
                "sender_id":self.scope["user"].id,
                "is_online":True,
            },
        )
        
        conversation = Conversation.objects.get(
            id=self.conversation_id
        )
        
        Message.objects.filter(
            conversation = conversation,
            is_read = False,
        ).exclude(
            sender=self.scope["user"],
        ).update(
            is_read = True,
        )
        
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                "type":"messages_read",
                "reader_id":self.scope["user"].id,
            },
        )

    def disconnect(self, close_code):
        self.scope["user"].is_online=False
        self.scope["user"].save(update_fields=["is_online"])
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                "type":"user_status",
                "sender_id":self.scope["user"].id,
                "is_online":False,
            },
        )
        
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
                "id":message.id,
                "message":message.message,
                "sender":user.first_name,
                "sender_id":user.id,
                "time":message.created_at.strftime("%d %b %H: %M"),
            }
        )
        
        
        conversation_data=json.dumps({
            "conversation_id":conversation.id,
            "message":message.message,
            "sender":user.first_name,
            "sender_id":user.id,
            "time":message.created_at.strftime("%d %b %H:%M"),
            
            "receiver_id":(
                conversation.provider.id
                if user == conversation.user
                else conversation.user.id
            ),
        })
        
        print("Sending coversation update")
        print(f"user_{conversation.user.id}")
        print(f"user_{conversation.provider.id}")
        
        async_to_sync(self.channel_layer.group_send)(
            f"user_{conversation.user.id}",
            {
                "type":"conversation_update",
                "text":conversation_data,
            },
        )
        
        async_to_sync(self.channel_layer.group_send)(
            f"user_{ conversation.provider.id }",
            {
                "type":"conversation_update",
                "text":conversation_data,
            },
        )
        
    def chat_message(self,event):
        message=event["message"],
        
        self.send(
            text_data=json.dumps({
                "type":"message",
                "id":event["id"],
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
        
        
    def messages_read(self,event):
        self.send(
            text_data=json.dumps({
                "type":"messages_read",
                "reader_id":event["reader_id"],
            })
        )
        
    def user_status(self,event):
        self.send(
            text_data=json.dumps({
                "type":"status",
                "sender_id":event["sender_id"],
                "is_online":event["is_online"],
            })
        )
        
        
    