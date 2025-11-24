from rest_framework import viewsets, permissions
from .models import Expense, SharedBudget, ChatMessage
from .serializers import ExpenseSerializer, SharedBudgetSerializer, ChatMessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SharedBudgetViewSet(viewsets.ModelViewSet):
    queryset = SharedBudget.objects.all()
    serializer_class = SharedBudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('created_at')
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Simple news proxy endpoint could be added here to call NewsAPI and summarize via a small summarizer.
from rest_framework.decorators import api_view
import requests

@api_view(['GET'])
def news_list(request):
    # placeholder: in production, call NewsAPI / Moneycontrol and return summarized cards
    data = [
        {'id':1,'title':'Markets stable', 'summary':'Equity markets saw moderate gains today...'},
        {'id':2,'title':'Interest rate update', 'summary':'RBI keeps repo rate unchanged...'}
    ]
    return Response(data)
# from django.contrib.auth.models import User
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken

# @api_view(['POST'])
# def signup(request):
#     data = request.data
#     if User.objects.filter(username=data['email']).exists():
#         return Response({"error": "Email already exists"}, status=400)
    
#     user = User.objects.create_user(username=data['email'], email=data['email'], password=data['password'], first_name=data.get('name',''))
#     user.save()
#     return Response({"message": "User created"}, status=201)


# @api_view(['POST'])
# def login(request):
#     data = request.data
#     user = authenticate(username=data['email'], password=data['password'])
#     if user:
#         refresh = RefreshToken.for_user(user)
#         return Response({"token": str(refresh.access_token)})
#     return Response({"error": "Invalid credentials"}, status=401)
