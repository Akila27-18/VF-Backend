# backend/chat/views.py
from django.http import JsonResponse
from .models import ChatMessage

def recent_messages(request):
    messages = ChatMessage.objects.order_by('-created_at')[:50]  # latest 50 messages
    data = [
        {
            "id": msg.id,
            "from_user": msg.from_user,
            "text": msg.text,
            "time": msg.time,
            "created_at": msg.created_at.isoformat(),
            "delivered": msg.delivered,
            "seen": msg.seen
        }
        for msg in reversed(messages)  # oldest first
    ]
    return JsonResponse(data, safe=False)
