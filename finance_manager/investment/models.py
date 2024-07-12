from django.db import models
from django.contrib.auth.models import User


class Investment(models.Model):
    CATEGORY_CHOICES = [
        ('Stock', 'Stocks'),
        ('Bond', 'Bonds'),
        ('Mutual Fund', 'Mutual Funds'),
        ('Real Estate', 'Real Estate'),
        ('Crypto', 'Cryptocurrency'),
        ('Retirement', 'Retirement Accounts'),
        ('Other', 'Other Investments'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"
