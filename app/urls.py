from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from app.views_auth import signup_view, login_view, password_reset_view
from app.views import ExpenseViewSet, SharedBudgetViewSet, ChatMessageViewSet, news_list

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'budgets', SharedBudgetViewSet, basename='budget')
router.register(r'chats', ChatMessageViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
    path('news/', news_list, name='news'),
    path('auth/signup/', signup_view, name='signup'),
    path('auth/login/', login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', password_reset_view, name='password_reset'),
]
