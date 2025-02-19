from django.urls import path
from .views import RegisterView, LoginView, ChatRoomListCreateView, MessageCreateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("chatrooms/", ChatRoomListCreateView.as_view(), name="chatrooms"),
 path("messages/create/", MessageCreateView.as_view(), name="message-create"),
]
