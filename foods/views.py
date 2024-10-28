from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Category, Food
from .serializers import CategorySerializer, FoodSerializer

# 카테고리 생성
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

# 음식 생성
class FoodCreateView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

# 카테고리 수정
class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

# 음식 수정
class FoodUpdateView(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]

# 카테고리 삭제
class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# 음식 삭제
class FoodDeleteView(generics.DestroyAPIView):
    queryset = Food.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# 모든 Category, Food 목록 조회 -> 누구나 접근 가능 하게(회의를 통해 변경할 수도 있음)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class FoodListView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]

# 카테고리에 해당하는 음식 조회
class FoodByCategoryView(generics.ListAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        category_name = request.query_params.get('name')
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                foods = self.get_queryset().filter(category=category)
                serializer = self.get_serializer(foods, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"detail": "해당 카테고리를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "카테고리 이름을 제공해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

# 음식 이름과 식당 이름에 해당하는 음식 조회
class FoodDetailByNameAndRestaurantView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        food_name = request.query_params.get('food_name')
        restaurant_name = request.query_params.get('restaurant_name')
        if food_name and restaurant_name:
            foods = self.queryset.filter(name=food_name, restaurant__name=restaurant_name)
            if foods.exists():
                serializer = self.get_serializer(foods, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "해당 음식이나 레스토랑을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "음식 이름과 레스토랑 이름을 제공해 주세요."}, status=status.HTTP_400_BAD_REQUEST)