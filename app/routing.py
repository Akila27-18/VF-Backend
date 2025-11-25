from django.urls import path
from .consumers import ChatConsumer, NewsConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
    path("ws/news/", NewsConsumer.as_asgi()),
]
