import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        self.sender_id = self.scope['user'].id
        self.room_name = f"chat_{min(self.sender_id, self.recipient_id)}_{max(self.sender_id, self.recipient_id)}"
        self.room_group_name = f"chat_{self.room_name}"

       
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']

        
        recipient = await sync_to_async(User.objects.get)(pk=self.recipient_id)
        await sync_to_async(Message.objects.create)(
            sender=sender,
            recipient=recipient,
            content=message
        )

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))
