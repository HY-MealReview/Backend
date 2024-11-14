from rest_framework import serializers
from .models import Rating
from foods.models import Food

class RatingSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True)  # 'food.name'을 출력하도록 설정

    class Meta:
        model = Rating
        fields = ['id', 'user', 'food_name', 'rating', 'created_at']  # food_name을 포함
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

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

class UserFoodRatingsSerializer(serializers.ModelSerializer):
    # ratings는 RatingSerializer로 처리하여 음식별 평가 정보 출력
    ratings = serializers.SerializerMethodField()
    # menus는 Food와 관련된 Menu 객체를 출력
    menus = serializers.SerializerMethodField()
    # 카테고리 이름
    category_name = serializers.CharField(source='category.name')
    # 식당 이름
    restaurant_name = serializers.CharField(source='restaurant.name')

    class Meta:
        model = Food
        fields = ['id', 'name', 'category_name', 'restaurant_name', 'ratings', 'menus']

    # ratings 필드는 로그인한 유저의 평가만 가져오는 메소드
    def get_ratings(self, obj):
        user = self.context.get('request').user  # 로그인한 유저 가져오기
        # 해당 음식에 대한 유저의 평점만 필터링
        ratings = obj.ratings.filter(user=user)
        return RatingSerializer(ratings, many=True).data

    # menus 필드는 관련된 Menu 객체들을 가져오는 메소드
    def get_menus(self, obj):
        # 해당 음식과 관련된 메뉴 정보들을 반환
        menus = obj.menus.all()
        return [{
            'date': menu.date,
            'time': menu.time,
            'restaurant_name': menu.restaurant.name
        } for menu in menus]
