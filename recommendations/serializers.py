from rest_framework import serializers
from .models import Recommendation
from restaurants.models import Menu, Restaurant

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['menu', 'recommendation']

class MenuRecommendationCountSerializer(serializers.ModelSerializer):
    menu_id = serializers.IntegerField(source='id', read_only=True) 
    true_count = serializers.IntegerField()
    false_count = serializers.IntegerField()
    restaurant = serializers.CharField(source='restaurant.name', read_only=True) 
    
    class Meta:
        model = Menu
        fields = ['menu_id', 'true_count', 'false_count', 'date', 'restaurant']

class UserMenuRecommendationSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = ['menu', 'recommendation']

    def get_menu(self, obj):
        return {
            'id': obj.menu.id,
            'date': obj.menu.date,
            'restaurant': obj.menu.restaurant.name
        }
