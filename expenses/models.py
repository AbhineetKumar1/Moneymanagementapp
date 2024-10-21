from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=266)

    def __str__(self):
        return f"{self.category} - {self.amount}"

    class Meta:
        ordering = ['-date']  # Changed ':' to '='

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name