# foods/models.py
from django.db import models
from restaurants.models import Restaurant

class Category(models.Model):
    category_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Food(models.Model):
    food_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='foods')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='foods')

    def __str__(self):
        return self.name
