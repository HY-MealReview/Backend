from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from restaurants.models import Restaurant, Menu
from ratings.models import Rating
from .models import Category, Food
from .serializers import CategorySerializer, FoodSerializer, FoodWithRatingsSummarySerializer, MenuWithFoodsSerializer

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
    queryset = Food.objects.all()  # 기본 쿼리셋 설정

    def get(self, request, *args, **kwargs):
        category_name = request.query_params.get('name')
        if category_name:
            category_name = category_name.rstrip('/')  # 슬래시 제거
            try:
                category = Category.objects.get(name=category_name)
                foods = self.queryset.filter(category=category)  # 필터링된 쿼리셋
                serializer = self.get_serializer(foods, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"detail": "해당 카테고리를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "카테고리 이름을 제공해 주세요."}, status=status.HTTP_400_BAD_REQUEST)


# 음식 이름과 식당 이름에 해당하는 음식 조회
class FoodDetailByNameAndRestaurantView(generics.ListAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        food_name = self.request.query_params.get('food_name', '').strip('/')
        restaurant_name = self.request.query_params.get('restaurant_name', '').strip('/')
        if food_name and restaurant_name:
            return Food.objects.filter(name=food_name, restaurant__name=restaurant_name)
        return Food.objects.none()

    def get(self, request, *args, **kwargs):
        food_name = request.query_params.get('food_name')
        restaurant_name = request.query_params.get('restaurant_name')
        if not (food_name and restaurant_name):
            return Response({"detail": "음식 이름과 레스토랑 이름을 제공해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        foods = self.get_queryset()
        if not foods.exists():
            return Response({"detail": "해당 음식이나 레스토랑을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 로그인 한 유저가 특정 식당 메뉴의 음식들에 매긴 평점들 모두 출력
class FoodRatingsListView(generics.ListAPIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get_queryset(self):
        # URL에서 쿼리 파라미터로 가져오기
        restaurant_name = self.request.query_params.get('restaurant_name', '').strip('/')
        date = self.request.query_params.get('date', '').strip('/')
        time = self.request.query_params.get('time', '').strip('/')

        # restaurant_name을 통해 Restaurant 객체 가져오기
        restaurant = get_object_or_404(Restaurant, name=restaurant_name)
        
        # 특정 restaurant, date, time에 따른 메뉴에 포함된 음식 조회
        menu = Menu.objects.filter(restaurant=restaurant, date=date, time=time).first()
        
        if menu:
            # 메뉴에 포함된 음식들을 가져오기
            return menu.foods.all()  # 음식 목록을 반환
        return Food.objects.none()  # 해당하는 메뉴가 없으면 빈 쿼리셋 반환

    def get(self, request, *args, **kwargs):
        # GET 요청 처리
        foods = self.get_queryset()
        if not foods.exists():
            return Response({"detail": "해당 날짜와 시간에 대한 메뉴가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 각 음식에 대한 id, name, ratings 포함한 데이터를 반환
        serializer = self.get_serializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 특정 식당의 어떤 메뉴에 속하는 음식들에 매긴 평점 출력  
class FoodWithRatingsSummaryByRestaurantMenuView(APIView):
    def get(self, request, *args, **kwargs):
        # URL에서 restaurant_name과 menu_date를 받아옵니다.
        restaurant_name = unquote(self.kwargs['restaurant_name'])
        menu_date = self.kwargs['menu_date']
        
        # 주어진 restaurant_name에 해당하는 restaurant를 찾습니다.
        restaurant = get_object_or_404(Restaurant, name=restaurant_name)
        
        # restaurant와 menu_date에 해당하는 메뉴들을 가져옵니다.
        menus = Menu.objects.filter(restaurant=restaurant, date=menu_date)
        
        if not menus.exists():
            return Response({"detail": "No menus found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 여러 메뉴에 해당하는 음식들을 가져옵니다.
        food_queryset = Food.objects.filter(menus__in=menus).prefetch_related('ratings')
        
        # 음식들을 그룹화해서 반환할 데이터 준비
        result = []
        for menu in menus:
            menu_foods = food_queryset.filter(menus=menu)
            food_data = FoodWithRatingsSummarySerializer(menu_foods, many=True).data
            
            result.append({
                'menu_id': menu.id,
                'menu_date': menu.date,
                'restaurant_name': restaurant.name,
                'time': menu.time,
                'foods': food_data
            })
        
        return Response(result)
