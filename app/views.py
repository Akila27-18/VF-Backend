from rest_framework import viewsets, permissions
from .models import Expense, SharedBudget, ChatMessage
from .serializers import ExpenseSerializer, SharedBudgetSerializer, ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated

# ---------------- Expense ----------------
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ---------------- SharedBudget ----------------
class SharedBudgetViewSet(viewsets.ModelViewSet):
    serializer_class = SharedBudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Budgets where user is a participant
        return SharedBudget.objects.filter(participants=self.request.user)

# ---------------- ChatMessage ----------------
class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Messages sent or received by the user
        return ChatMessage.objects.filter(sender=user) | ChatMessage.objects.filter(receiver=user)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def news_api(request):
    news = [
        {
            "id": 1,
            "title": "Markets stable",
            "summary": f"Equity markets saw gains at {datetime.now().strftime('%H:%M:%S')}"
        },
        {
            "id": 2,
            "title": "Interest rate update",
            "summary": f"RBI keeps repo rate unchanged at {datetime.now().strftime('%H:%M:%S')}"
        }
    ]
    return Response(news)
