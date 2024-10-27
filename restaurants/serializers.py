from rest_framework import serializers
from .models import Restaurant, Menu
from foods.models import Food

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']

class MenuSerializer(serializers.ModelSerializer):
    foods = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'date', 'restaurant', 'foods']

    def create(self, validated_data):
        # 유효성 검사된 데이터에서 레스토랑 정보를 추출
        restaurant_data = validated_data.pop('restaurant')
        menu = Menu.objects.create(restaurant=restaurant_data, **validated_data)
        return menu
