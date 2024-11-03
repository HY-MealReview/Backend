# restaurants/models.py
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    TIME_CHOICES = [
        ('조식', '조식'),
        ('중식', '중식'),
        ('석식', '석식'),
    ]

    date = models.DateField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    foods = models.ManyToManyField('foods.Food', related_name='menus')  # Food와 다대다 관계
    photo = models.ImageField(upload_to='menu_photos/', null=True, blank=True)
    time = models.CharField(max_length=10, choices=TIME_CHOICES)  # 추가된 필드

    def __str__(self):
        return f"Menu for {self.restaurant.name} on {self.date}"
