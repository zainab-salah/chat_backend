import os
import django

# ✅ Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ✅ Initialize Django before importing anything else
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.middleware import JWTAuthMiddleware  # ✅ Import new middleware
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        JWTAuthMiddleware(  # ✅ Apply middleware to authenticate WebSocket users
            URLRouter(chat.routing.websocket_urlpatterns)
        )
    ),
})
