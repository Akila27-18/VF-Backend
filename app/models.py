from django.db import models

# ---------------- Simple User ----------------
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # store hashed passwords in production

    def __str__(self):
        return self.username

# ---------------- Expense ----------------
class Expense(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

# ---------------- Shared Budget ----------------
class SharedBudget(models.Model):
    name = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ---------------- Chat Message ----------------
class ChatMessage(models.Model):
    from_user = models.CharField(max_length=120, default="Anonymous")
    text = models.TextField()
    time = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.text[:20]}"

