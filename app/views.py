from rest_framework import viewsets, permissions
from .models import Expense, SharedBudget, ChatMessage
from .serializers import ExpenseSerializer, SharedBudgetSerializer, ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated

# ---------------- Expense ----------------
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only expenses owned by the user
        return Expense.objects.filter(owner=self.request.user)

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
