from django.urls import path
from .views import (
    RegisterView, LoginView, ChatRoomListCreateView,
    MessageCreateView, MessageListView, MessageDeleteView,ChatRoomDeleteView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("chatrooms/", ChatRoomListCreateView.as_view(), name="chatrooms"),
    path("chatrooms/delete/<int:room_id>/", ChatRoomDeleteView.as_view(), name="chatroom-delete"),
    path("messages/create/", MessageCreateView.as_view(), name="message-create"),
    path("messages/<int:room_id>/", MessageListView.as_view(), name="message-list"),  
    path("messages/delete/<int:message_id>/", MessageDeleteView.as_view(), name="message-delete"), 
]
