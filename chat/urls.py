from django.urls import path
from .views import RegisterView, LoginView, ChatRoomListCreateView, MessageListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatrooms'),
    path('chatrooms/<str:room_id>/messages/', MessageListView.as_view(), name='messages'),
]