import json
import uuid
import jwt
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

     
        token = self.scope["query_string"].decode().split("token=")[-1]
        self.user = None

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                self.user = await self.get_user(payload["user_id"])
            except jwt.ExpiredSignatureError:
                await self.close()
                return
            except jwt.InvalidTokenError:
                await self.close()
                return

        if not self.user:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_content = data.get("message")

            if not message_content:
                return

            if not self.user:
                return

            event = {
                "type": "chat_message",
                "room_id": self.room_id,
                "user": self.user.username,
                "message": message_content,
                "id": str(uuid.uuid4()),
                "date": datetime.now().isoformat(),
            }

            await self.channel_layer.group_send(self.room_group_name, event)

        except json.JSONDecodeError as e:
            pass

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def get_user(self, user_id):
        """Fetch user from DB asynchronously"""
        return await User.objects.filter(id=user_id).afirst()
