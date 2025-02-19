from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, ChatRoomSerializer, MessageSerializer
from .models import ChatRoom, Message
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


# Utility function for JWT tokens
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# ✅ Login API
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user:
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "tokens": get_tokens(user),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

# ✅ Register API (Now Uses `UserSerializer`)
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"user": UserSerializer(user).data, "tokens": get_tokens(user)},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Chat Rooms API
class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]


# Messages API for a Chat Room
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")

        if not ChatRoom.objects.filter(id=room_id).exists():
            return Message.objects.none()

        return Message.objects.filter(chatroom_id=room_id).order_by("timestamp")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(
            {"messages": MessageSerializer(queryset, many=True).data},
            status=status.HTTP_200_OK,
        )


class MessageCreateView(CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        chatroom_id = request.data.get("chatroom_id")
        content = request.data.get("content")

        if not chatroom_id or not content:
            return Response(
                {"error": "chatroom_id and content are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {"error": "Chatroom not found."}, status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            user=request.user, chatroom=chatroom, content=content
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
