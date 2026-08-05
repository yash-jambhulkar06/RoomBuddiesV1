from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ConversationConsumer(WebsocketConsumer):
    # def connect(self):
    #     self.group_name = f"user_{self.scope['user'].id}"

    #     async_to_sync(self.channel_layer.group_add)(
    #         self.group_name,
    #         self.channel_name,
    #     )

    #     self.accept()
    
    def connect(self):
        print("=== ConversationConsumer CONNECT ===")
        print("User:", self.scope["user"])
        print("Authenticated:", self.scope["user"].is_authenticated)

        self.group_name = f"user_{self.scope['user'].id}"

        async_to_sync(self.channel_layer.group_add)(
        self.group_name,
        self.channel_name,
        )

        self.accept()

        print("Connection accepted")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def conversation_update(self, event):
        self.send(text_data=event["text"])