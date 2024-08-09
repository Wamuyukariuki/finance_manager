from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now().date())

    def __str__(self):
        return f"{self.user.username} - KES {self.amount}"