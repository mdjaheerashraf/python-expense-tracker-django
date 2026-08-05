from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Travel', 'Travel'),
    ('Shopping', 'Shopping'),
    ('Bills', 'Bills'),
    ('Others', 'Others'),
]


class Expense(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    title = models.CharField(max_length=50)

    amount = models.FloatField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    date = models.DateField()

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title