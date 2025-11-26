# vetri_backend/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from app.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vetri_backend.settings")

# IMPORTANT: Init Django before Channels loads routes
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
