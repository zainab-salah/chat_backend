import json
import uuid
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import ChatRoom, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
 
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return

 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

 
        chat_history = await self.get_chat_history(self.room_id)
        await self.send(text_data=json.dumps({"chat_history": chat_history}))

    async def disconnect(self, close_code):
 
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json.get('message')

            if not message_content:
                await self.send(json.dumps({'error': 'Message content is required.'}))
                return

        
            if self.user.is_anonymous:
                await self.send(json.dumps({'error': 'Authentication required.'}))
                return

        
            message = await self.save_message(self.room_id, self.user, message_content)

      
            event = {
                'type': 'chat_message',
                'room_id': self.room_id,
                'user': self.user.username,
                'message': message_content,
                'id': str(uuid.uuid4()),  
                'date': message.timestamp.isoformat(),
            }

            await self.channel_layer.group_send(self.room_group_name, event)  

        except json.JSONDecodeError as e:
            await self.send(json.dumps({'error': f'Invalid JSON format: {str(e)}'}))

    async def chat_message(self, event):
      
        await self.send(text_data=json.dumps({
            'room_id': event['room_id'],
            'user': event['user'],
            'message': event['message'],
            'id': event['id'],
            'date': event['date'],
        }))

    @sync_to_async
    def save_message(self, room_id, user, message_content):
        """Save the new message to the database"""
        #chatroom, created = ChatRoom.objects.get_or_create(name=room_id)
        chatroom, created = ChatRoom.objects.get_or_create(name=room_id, defaults={"creator": user})

        message = Message.objects.create(
            user=user,
            chatroom=chatroom,
            content=message_content
        )
        return message

    @sync_to_async
    def get_chat_history(self, room_id):
        """Fetch the last 50 messages from the database"""
        chatroom = ChatRoom.objects.filter(name=room_id).first()
        if not chatroom:
            return []

        messages = Message.objects.filter(chatroom=chatroom).order_by("-timestamp")[:50]
        return MessageSerializer(messages, many=True).data
