from .consumers import ChatConsumer, NewsConsumer, DashboardConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
    path("ws/news/", NewsConsumer.as_asgi()),
    path("ws/dashboard/", DashboardConsumer.as_asgi()),
]
