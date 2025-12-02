from django.conf import settings
from django.db import models

class ChatMessage(models.Model):
    from_user = models.CharField(max_length=120, default="Anonymous")
    text = models.TextField()
    time = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.sender.username}: {self.text[:40]}"
