from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import ChatRoom, Message

class Command(BaseCommand):
    help = 'Seed the database with some messages'

    def handle(self, *args, **kwargs):
 
        user, created = User.objects.get_or_create(username='test', defaults={'password': 'qwe123'})

 
        chat_room, created = ChatRoom.objects.get_or_create(id=1, defaults={'name': 'Test Room'})

 
        messages = [
            "Hello, this is a test message.",
            "How are you doing today?",
            "This is another test message.",
            "Let's chat in this room.",
            "This is the last test message."
        ]

        for content in messages:
            Message.objects.create(user=user, chatroom=chat_room, content=content)

        self.stdout.write(self.style.SUCCESS('Successfully seeded messages'))