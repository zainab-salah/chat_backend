
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ChatRoomListCreateView, MessageListView
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
       path("chatrooms/", ChatRoomListCreateView.as_view(), name="chatroom-list-create"),
         path("messages/<str:room_name>/", MessageListView.as_view(), name="message-list"),
]

