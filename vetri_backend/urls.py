# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('app.urls')),   # your main API
# ]
# vetri_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app.views import ExpenseViewSet, SharedBudgetViewSet, ChatMessageViewSet, news_list
from app.views_auth import signup_view, login_view, password_reset_view
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', SharedBudgetViewSet)
router.register(r'chats', ChatMessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('news/', news_list),

    # Auth
    path('auth/signup/', signup_view, name='signup'),
    path('auth/login/', login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', password_reset_view, name='password_reset'),
]
