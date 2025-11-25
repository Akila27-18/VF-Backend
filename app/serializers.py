from rest_framework import serializers
from .models import Expense, SharedBudget, ChatMessage
from django.contrib.auth.models import User

# ---------------- Expense ----------------
class ExpenseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # auto-set from request.user

    class Meta:
        model = Expense
        fields = '__all__'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

# ---------------- SharedBudget ----------------
class SharedBudgetSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = SharedBudget
        fields = '__all__'

# ---------------- ChatMessage ----------------
class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')  # auto-set from request.user
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'text', 'expense', 'seen', 'created_at']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

# ---------------- User ----------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
