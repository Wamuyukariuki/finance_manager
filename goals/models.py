from django.db import models
from django.contrib.auth.models import User

class Goals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Field added for saved amount
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_progress(self):
        if self.target_amount == 0:
            return 0.0
        return (self.current_amount / self.target_amount) * 100
