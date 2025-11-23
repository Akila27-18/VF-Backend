from django.urls import path, include
from rest_framework import routers
from .views import ExpenseViewSet, SharedBudgetViewSet, ChatMessageViewSet, news_list
from .views_auth import signup, login_view, password_reset
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', SharedBudgetViewSet)
router.register(r'chats', ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('news/', news_list),

    # Auth
    path('auth/signup/', signup),
    path('auth/login/', login_view),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', password_reset),
]
