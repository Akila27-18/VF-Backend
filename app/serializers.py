from rest_framework import serializers
from .models import Expense, SharedBudget, ChatMessage
from django.contrib.auth.models import User

class ExpenseSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Expense
        fields = '__all__'

class SharedBudgetSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    class Meta:
        model = SharedBudget
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'text', 'expense', 'seen', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
