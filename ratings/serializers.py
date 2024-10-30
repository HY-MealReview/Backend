# ratings/serializers.py
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
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ['id', 'name', 'average_rating', 'rating_count']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            total_rating = sum(r.rating for r in ratings)
            return total_rating / ratings.count()
        return 0

    def get_rating_count(self, obj):
        return obj.ratings.count()

class UserFoodRatingsSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'ratings']
