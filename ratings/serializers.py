from rest_framework import serializers
from .models import Rating
from foods.models import Food

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'food', 'rating']
        read_only_fields = ['user']

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
    ratings = RatingSerializer(many=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'ratings']
