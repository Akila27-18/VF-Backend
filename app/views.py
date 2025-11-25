from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Expense, SharedBudget, ChatMessage
from .serializers import ExpenseSerializer, SharedBudgetSerializer, ChatMessageSerializer

# Expenses
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user).order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Shared Budgets
class SharedBudgetViewSet(viewsets.ModelViewSet):
    serializer_class = SharedBudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return SharedBudget.objects.filter(participants=self.request.user).order_by('-created_at')
    def perform_create(self, serializer):
        budget = serializer.save()
        budget.participants.add(self.request.user)

# Chat Messages
class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ChatMessage.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).order_by('created_at')
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# News
@api_view(['GET'])
def news_list(request):
    data = [
        {'id': 1, 'title': 'Markets stable', 'summary': 'Equity markets saw moderate gains today...'},
        {'id': 2, 'title': 'Interest rate update', 'summary': 'RBI keeps repo rate unchanged...'}
    ]
    return Response(data)
