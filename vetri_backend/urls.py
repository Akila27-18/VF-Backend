# vetri_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),  # your router URLs

    # JWT auth endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom signup
    path('auth/signup/', app_views.signup, name='signup'),
]
