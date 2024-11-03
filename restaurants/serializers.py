from rest_framework import serializers
from .models import Restaurant, Menu
from foods.models import Food

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']

class MenuSerializer(serializers.ModelSerializer):
    foods = serializers.PrimaryKeyRelatedField(many=True, queryset=Food.objects.all())  # 수정: foods를 쓰기 가능하게
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Menu
        fields = ['id', 'date', 'restaurant', 'foods', 'photo', 'time']

    def create(self, validated_data):
        # 유효성 검사된 데이터에서 foods를 분리
        foods_data = validated_data.pop('foods')
        menu = Menu.objects.create(**validated_data)  # Menu 객체 생성
        
        # foods를 Menu에 추가
        menu.foods.set(foods_data)  # 다대다 관계를 설정

        return menu
