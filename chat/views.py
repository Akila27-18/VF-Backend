from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from django.utils.dateparse import parse_datetime

@api_view(["GET"])
def recent_messages(request):
    """
    GET /api/messages?before=ISO_DATE&limit=20
    """
    limit = int(request.GET.get("limit", 20))
    before = request.GET.get("before")
    qs = ChatMessage.objects.order_by("-created_at")
    if before:
        dt = parse_datetime(before)
        if dt:
            qs = qs.filter(created_at__lt=dt)
    msgs = qs[:limit]
    serializer = ChatMessageSerializer(msgs, many=True)
    return Response(serializer.data)
