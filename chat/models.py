from django.db import models

class ChatMessage(models.Model):
    from_user = models.CharField(max_length=255)
    text = models.TextField()
    time = models.CharField(max_length=50)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user}: {self.text[:20]}"
