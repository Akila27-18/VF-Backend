# app/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Expense, SharedBudget, ChatMessage
from .serializers import ExpenseSerializer, SharedBudgetSerializer, ChatMessageSerializer
from django.contrib.auth.models import User

# ------------------ Expenses ------------------
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the owner
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Users see only their own expenses
        return Expense.objects.filter(owner=self.request.user).order_by('-created_at')


# ------------------ Shared Budgets ------------------
class SharedBudgetViewSet(viewsets.ModelViewSet):
    queryset = SharedBudget.objects.all()
    serializer_class = SharedBudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        budget = serializer.save()
        # Optionally add the creator to participants
        budget.participants.add(self.request.user)


# ------------------ Chat Messages ------------------
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('created_at')
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set sender to logged-in user
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        # Users see messages they are involved in
        return ChatMessage.objects.filter(
            models.Q(sender=self.request.user) | models.Q(receiver=self.request.user)
        ).order_by('created_at')


# ------------------ News Endpoint ------------------
@api_view(['GET'])
def news_list(request):
    data = [
        {'id':1,'title':'Markets stable', 'summary':'Equity markets saw moderate gains today...'},
        {'id':2,'title':'Interest rate update', 'summary':'RBI keeps repo rate unchanged...'}
    ]
    return Response(data)
