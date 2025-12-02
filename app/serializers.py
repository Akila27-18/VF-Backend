from rest_framework import serializers
from .models import Expense, SharedBudget, ChatMessage, User  # import your custom User

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class SharedBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedBudget
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # use your custom User
        fields = ['id', 'username', 'password']  # add password if needed
        extra_kwargs = {'password': {'write_only': True}}  # don't expose password in GET responses
