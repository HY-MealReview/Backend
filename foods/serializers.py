# foods/serializers.py
from rest_framework import serializers
from .models import Category, Food

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id','name', 'category', 'restaurant']