from django.urls import path, include
from rest_framework import routers
from .views import (
    ExpenseViewSet,
    SharedBudgetViewSet,
    ChatMessageViewSet,
    news_list,
    signup,
    login
)

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', SharedBudgetViewSet)
router.register(r'chats', ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('news/', news_list),
    path('signup/', signup),
    path('login/', login),
]
