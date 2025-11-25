# app/routing.py
from django.urls import re_path
from .consumers import ChatConsumer, NewsConsumer, DashboardConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
    re_path(r"ws/news/$", NewsConsumer.as_asgi()),
    re_path(r"ws/dashboard/$", DashboardConsumer.as_asgi()),
]
