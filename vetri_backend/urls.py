from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),        # REST API for app
    path('api/chat/', include('chat.urls')),  # REST API for chat messages (optional)
]
