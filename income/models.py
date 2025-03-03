from django.db import models
from django.contrib.auth.models import User


class Income(models.Model):
    CATEGORY_CHOICES = [
        ('Salary', 'Salary/Wages'),
        ('Bonus', 'Bonuses'),
        ('Interest', 'Interest Income'),
        ('Dividend', 'Dividends'),
        ('Rental', 'Rental Income'),
        ('Freelance', 'Freelance/Gig Income'),
        ('Other', 'Other Income Sources'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    needs_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=50)
    wants_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    savings_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20)

    def __str__(self):
        return f"{self.user.username}'s Profile"