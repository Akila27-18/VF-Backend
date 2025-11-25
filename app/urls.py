from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ExpenseViewSet,
    SharedBudgetViewSet,
    ChatMessageViewSet,
    news_api   # ⬅ ADD THIS
)

from .views_auth import signup_view, login_view, password_reset_view

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'shared-budgets', SharedBudgetViewSet, basename='sharedbudget')
router.register(r'chat-messages', ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    # Authentication
    path('auth/signup/', signup_view),
    path('auth/login/', login_view),
    path('auth/password-reset/', password_reset_view),

    # News API endpoint
    path('news/', news_api),     # ⬅ THIS FIXES THE 404 ERROR

    # Viewsets
    path('', include(router.urls)),
]
