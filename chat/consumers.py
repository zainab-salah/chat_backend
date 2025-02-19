import json
import uuid
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

      
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
        try:
            text_data_json = json.loads(text_data)

 
            user = text_data_json.get('user')
            message = text_data_json.get('message')

            if not user or not message:
                await self.send(json.dumps({'error': 'Missing user or message field'}))
                return
 
            message_id = str(uuid.uuid4())  
            date = datetime.now().isoformat()   

 
            event = {
                'type': 'chat_message',
                'room_id': self.room_name,
                'user': user,
                'message': message,
                'id': message_id,   
                'date': date,
            }

 
            print("Sending Event to Group:", event)
 
            await self.channel_layer.group_send(self.room_group_name, event)

        except json.JSONDecodeError as e:
            await self.send(json.dumps({'error': f'Invalid JSON format: {str(e)}'}))

    async def chat_message(self, event):
 
        required_fields = ['room_id', 'user', 'message', 'id', 'date']
        if not all(field in event for field in required_fields):
            print("ERROR: Missing fields in event", event)   
            return
 
        await self.send(text_data=json.dumps({
            'room_id': event['room_id'],
            'user': event['user'],
            'message': event['message'],
            'id': event['id'],  
            'date': event['date'],  
        }))

