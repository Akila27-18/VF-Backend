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
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
import jwt
from django.conf import settings

JWT_SECRET = settings.SECRET_KEY

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username, password=make_password(password))
    user.save()
    token = jwt.encode({'id': user.id}, JWT_SECRET, algorithm='HS256')
    return Response({'token': token, 'username': user.username})

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token = jwt.encode({'id': user.id}, JWT_SECRET, algorithm='HS256')
    return Response({'token': token, 'username': user.username})
