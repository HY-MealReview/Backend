# restaurants/models.py
from django.db import models
from foods.models import Food

class Restaurant(models.Model):
    restaurant_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Menu(models.Model):
    menu_id = models.CharField(max_length=10, primary_key=True)
    date = models.DateField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    foods = models.ManyToManyField(Food, related_name='menus')  # Food와 다대다 관계

    def __str__(self):
        return f"Menu for {self.restaurant.name} on {self.date}"
