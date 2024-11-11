# foods/serializers.py
from rest_framework import serializers
from ratings.models import Rating
from restaurants.models import Menu
from .models import Category, Food, Restaurant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating']  # 평점만 출력      

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name']  # 식당 이름만 반환  

class FoodSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  
    category_name = serializers.CharField(source='category.name', read_only=True)  # Category의 name을 추가
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)  # Restaurant의 name을 추가
    ratings = RatingSerializer(many=True, read_only=True) 

    class Meta:
        model = Food
        fields = ['id','name', 'category', 'category_name', 'restaurant', 'restaurant_name', 'ratings']

    def create(self, validated_data):
        return Food.objects.create(**validated_data)
