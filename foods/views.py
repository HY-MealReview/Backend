# foods/views.py
from rest_framework import generics, permissions
from .models import Category, Food
from .serializers import CategorySerializer, FoodSerializer

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

class FoodCreateView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능
