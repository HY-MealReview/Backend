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
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        restaurant_name = self.request.query_params.get('restaurant')
        menu_date = self.request.query_params.get('date')

        if menu_date and menu_date.endswith('/'):
            menu_date = menu_date.rstrip('/')

        if restaurant_name and menu_date:
            return self.queryset.filter(restaurant__name=restaurant_name, date=menu_date)
        return Menu.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "해당 레스토랑의 메뉴가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        data = [
            {
                "id": menu.id,
                "restaurant": menu.restaurant.name,
                "date": menu.date,
                "time": menu.time, 
                "photo": menu.photo.url if menu.photo else None,  # photo 필드 추가
                "foods": list(menu.foods.all().values_list('name', flat=True))
            }
            for menu in queryset
        ]
        
        return Response(data)

# 10. 특정 메뉴 ID를 입력하면 해당 메뉴의 정보 출력 (관리자 계정만 가능)
class MenuDetailByIdView(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자 계정만 접근 가능하도록 설정

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Menu 객체 가져오기
        data = {
            "id": instance.id,
            "restaurant": instance.restaurant.name,
            "date": instance.date,
            "time": instance.time, 
            "photo": instance.photo.url if menu.photo else None,
            "foods": list(instance.foods.all().values_list('name', flat=True))  # 음식 이름만 리스트로 가져오기
        }
        return Response(data)

# 11. 식당 이름과 날짜, 타임으로 메뉴 조회
class MenuSearchView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        restaurant_name = self.request.query_params.get('restaurant')
        menu_date = self.request.query_params.get('date')
        time = self.request.query_params.get('time')

        if time and time.endswith('/'):
            time = time.rstrip('/')

        if restaurant_name and menu_date and time:
            return self.queryset.filter(
                restaurant__name=restaurant_name,
                date=menu_date,
                time=time
            )
        return Menu.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "해당 레스토랑의 메뉴가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                "id": menu.id,
                "restaurant": menu.restaurant.name,
                "date": menu.date,
                "time": menu.time,  # 타임 필드 추가
                "photo": menu.photo.url if menu.photo else None,
                "foods": list(menu.foods.all().values_list('name', flat=True))
            }
            for menu in queryset
        ]
        
        return Response(data)

# 12. 날짜와 타임으로 메뉴 조회
class MenuSearchByTimeView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        menu_date = self.request.query_params.get('date')
        time = self.request.query_params.get('time')

        if time and time.endswith('/'):
            time = time.rstrip('/')

        if menu_date and time:
            return self.queryset.filter(date=menu_date, time=time)
        return Menu.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "해당 메뉴가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                "id": menu.id,
                "restaurant": menu.restaurant.name,
                "date": menu.date,
                "time": menu.time,  # 타임 필드 추가
                "photo": menu.photo.url if menu.photo else None,
                "foods": list(menu.foods.all().values_list('name', flat=True))
            }
            for menu in queryset
        ]
        
        return Response(data)