from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, SharedBudgetViewSet, ChatMessageViewSet
from .views_auth import signup_view, login_view, password_reset_view

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'shared-budgets', SharedBudgetViewSet, basename='sharedbudget')
router.register(r'chat-messages', ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('auth/signup/', signup_view),
    path('auth/login/', login_view),
    path('auth/password-reset/', password_reset_view),
    path('', include(router.urls)),
]
