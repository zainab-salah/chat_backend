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

        # Extract token from query params
        token = self.scope["query_string"].decode().split("token=")[-1]
        self.user = None

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                self.user = await self.get_user(payload["user_id"])  # ✅ Fix: Call method inside the class
            except jwt.ExpiredSignatureError:
    #            print("❌ Token expired, closing WebSocket.")
                await self.close()
                return
            except jwt.InvalidTokenError:
     #           print("❌ Invalid token, closing WebSocket.")
                await self.close()
                return

        if not self.user:
     #       print("❌ Anonymous user, closing WebSocket.")
            await self.close()
            return

  #      print(f"✅ WebSocket Connected: {self.user.username} joined {self.room_id}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
      #  print(f"🟢 WebSocket accepted for room {self.room_id}")

    async def disconnect(self, close_code):
    #    print(f"🔴 WebSocket Disconnected: {self.room_id}, Code: {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
  #      print(f"📩 Message received: {text_data}")

        try:
            data = json.loads(text_data)
            message_content = data.get("message")

            if not message_content:
  #           
                return

            if not self.user:
  #              print("❌ Unauthorized user, message ignored.")
                return
            print(f"✅ {self.user.username} joined group {self.room_group_name}")

            event = {
                "type": "chat_message",
                "room_id": self.room_id,
                "user": self.user.username,
                "user_id": self.user.id,
                "message": message_content,
                "id": str(uuid.uuid4()),
                "date": datetime.now().isoformat(),
            }

            print(f"📢 Broadcasting message to room {event['room_id']}")

            await self.channel_layer.group_send(self.room_group_name, event)

        except json.JSONDecodeError as e:
           print(f"❌ Error parsing message: {e}")

    async def chat_message(self, event):
  #      print(f"📤 Sending message to WebSocket clients: {event}")
        await self.send(text_data=json.dumps(event))

    async def get_user(self, user_id):  # ✅ Fix: This method must be inside the class
        """Fetch user from DB asynchronously"""
        return await User.objects.filter(id=user_id).afirst()
