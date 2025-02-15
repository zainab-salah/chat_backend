import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        token = self.scope['query_string'].decode('utf-8').split('=')[-1]
        print(token)

        try:
            access_token = AccessToken(token)
            self.user = await database_sync_to_async(User.objects.get)(id=access_token['user_id'])
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"

            # Add user to group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

        except Exception:
         
            await self.close()

    async def disconnect(self, close_code):
   
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = self.user.username


        await database_sync_to_async(Message.objects.create)(
            user=self.user, chatroom=ChatRoom.objects.get(name=self.room_name), content=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({"message": message, "username": username}))
