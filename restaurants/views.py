from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer

class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

class MenuCreateView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

class MenuDetailView(generics.ListAPIView):  # ListAPIView를 사용해 필터링된 메뉴 목록을 조회
    serializer_class = MenuSerializer

    def get_queryset(self):
        # URL에서 restaurant의 이름과 날짜를 가져옴
        restaurant_name = self.request.query_params.get('restaurant')
        menu_date = self.request.query_params.get('date')
        
        # restaurant 이름과 date로 Menu 필터링
        queryset = Menu.objects.filter(restaurant__name=restaurant_name, date=menu_date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "해당 레스토랑의 메뉴가 없습니다."}, status=404)
        
        # 요청한 메뉴의 음식 이름들을 출력
        menu = queryset.first()
        foods = menu.foods.all().values_list('name', flat=True)  # Menu에 연결된 Food의 이름만 추출
        data = {
            "restaurant": menu.restaurant.name,
            "date": menu.date,
            "foods": list(foods)
        }
        return Response(data)

