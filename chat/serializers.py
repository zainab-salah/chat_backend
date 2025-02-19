from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatRoom, Message
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  


 


class ChatRoomSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'created_at', 'creator']



 
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chatroom", "user", "content", "timestamp"]  
        read_only_fields = ["id", "timestamp", "user"]  

    def create(self, validated_data):
        request = self.context.get("request")   
        validated_data["user"] = request.user  
        return super().create(validated_data)
