from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ChatRoomSerializer,
    MessageSerializer,
)
from rest_framework import generics, permissions
from .models import ChatRoom, Message


# Generate JWT token
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


from django.contrib.auth import authenticate


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
        if user is not None:
            return Response(
                {"user": UserSerializer(user).data, "tokens": get_tokens(user)},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# Register API
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
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


# Create & List Chat Rooms
class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "No chat rooms found."}, status=status.HTTP_200_OK
            )
        return super().list(request, *args, **kwargs)


# List Messages in a Chat Room


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]

        if not ChatRoom.objects.filter(id=room_id).exists():
            return Message.objects.none()

        return Message.objects.filter(chatroom_id=room_id).order_by("timestamp")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"messages": []}, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]

        if not ChatRoom.objects.filter(id=room_id).exists():
            return Message.objects.none()

        return Message.objects.filter(chatroom_id=room_id).order_by("timestamp")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"messages": []}, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]

        if not ChatRoom.objects.filter(id=room_id).exists():
            return Message.objects.none()

        return Message.objects.filter(chatroom_id=room_id).order_by("timestamp")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]

        if not ChatRoom.objects.filter(id=room_id).exists():
            return Message.objects.none()

        return Message.objects.filter(chatroom_id=room_id).order_by("timestamp")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]

        if not ChatRoom.objects.filter(id=room_id).exists():
            return Message.objects.none()

        return Message.objects.filter(chatroom__id=room_id).order_by("timestamp")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)
