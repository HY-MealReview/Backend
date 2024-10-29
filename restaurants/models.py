# restaurants/models.py
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    date = models.DateField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    foods = models.ManyToManyField('foods.Food', related_name='menus')  # Food와 다대다 관계

    def __str__(self):
        return f"Menu for {self.restaurant.name} on {self.date}"
