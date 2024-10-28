from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer

# 1. 식당 생성 (관리자 계정만 생성 가능)
class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminUser]

# 2. 식당 수정 (관리자 계정만 수정 가능)
class RestaurantUpdateView(generics.UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminUser]

# 3. 식당 삭제 (관리자 계정만 삭제 가능)
class RestaurantDeleteView(generics.DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminUser]

# 4. 모든 식당 정보 조회 (admin 계정만 가능)
class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminUser]

# 5. 메뉴 생성 (관리자 계정만 생성 가능)
class MenuCreateView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]

# 6. 메뉴 수정 (관리자 계정만 수정 가능)
class MenuUpdateView(generics.UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]

# 7. 메뉴 삭제 (관리자 계정만 삭제 가능)
class MenuDeleteView(generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]

# 8. 모든 메뉴 정보 조회 (관리자 계정만 가능)
class MenuListView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]

# 9. 특정 식당 이름과 날짜를 입력하면 해당하는 메뉴의 음식 정보 출력 (로그인 없어도 가능)
class MenuDetailView(generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        restaurant_name = self.request.query_params.get('restaurant')
        menu_date = self.request.query_params.get('date')

        queryset = Menu.objects.filter(restaurant__name=restaurant_name, date=menu_date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "해당 레스토랑의 메뉴가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 요청한 메뉴의 음식 이름들을 출력
        menu = queryset.first()
        foods = menu.foods.all().values_list('name', flat=True)
        data = {
            "restaurant": menu.restaurant.name,
            "date": menu.date,
            "foods": list(foods)
        }
        return Response(data)

# 10. 특정 식당에 특정 날짜에 해당하는 메뉴에 음식 정보 넣기 (ManyToManyField)
class MenuAddFoodView(generics.UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        menu = self.get_object()
        foods = request.data.get('foods', None)

        if foods is not None:
            # ManyToManyField에 음식 추가
            menu.foods.add(*foods)  # unpacking으로 리스트 추가
            menu.save()
            return Response({"detail": "음식이 메뉴에 추가되었습니다."}, status=status.HTTP_200_OK)

        return Response({"detail": "음식 리스트가 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
