from django.db import models

class ChatMessage(models.Model):
    from_user = models.CharField(max_length=255)       # sender name
    text = models.TextField()                           # message text
    time = models.CharField(max_length=50)             # display time e.g., "10:30 AM"
    seen = models.BooleanField(default=False)          # has this message been seen?
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]                      # always return messages in chronological order

    def __str__(self):
        # Show first 20 chars for display
        return f"{self.from_user}: {self.text[:20]}"
