# foods/models.py
from django.db import models
from restaurants.models import Restaurant

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='foods')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='foods')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'restaurant'], name='unique_food_name_per_restaurant')
        ]

    def __str__(self):
        return self.name
