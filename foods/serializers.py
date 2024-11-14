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
        fields = ['rating', 'created_at']  # 평점만 출력      

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


class FoodRatingSummarySerializer(serializers.ModelSerializer):
    total_rating = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ['id', 'name', 'total_rating', 'average_rating', 'users_count']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            total_rating = sum(r.rating for r in ratings)
            return total_rating / ratings.count()
        return 0

    def get_total_rating(self, obj):
        return sum(r.rating for r in obj.ratings.all())

    def get_users_count(self, obj):
        return obj.ratings.values('user').distinct().count()

class FoodWithRatingsSummarySerializer(FoodRatingSummarySerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)  # 카테고리 이름
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)  # 레스토랑 이름
    menu_date = serializers.DateField(source='menu.date', read_only=True)  # 메뉴 날짜
    menu_time = serializers.CharField(source='menu.time', read_only=True)  # 메뉴 시간

    class Meta:
        model = Food
        fields = FoodRatingSummarySerializer.Meta.fields + ['category_name', 'restaurant_name', 'menu_date', 'menu_time']


# 메뉴에 속하는 음식들을 그룹화하는 Serializer
class MenuWithFoodsSerializer(serializers.Serializer):
    menu_date = serializers.DateField()
    restaurant_name = serializers.CharField()
    time = serializers.CharField()
    foods = FoodWithRatingsSummarySerializer(many=True)

    class Meta:
        fields = ['menu_date', 'restaurant_name', 'time', 'foods']