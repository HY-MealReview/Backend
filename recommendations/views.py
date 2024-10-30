from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Recommendation
from restaurants.models import Menu
from .serializers import (
    RecommendationSerializer, 
    MenuRecommendationCountSerializer, 
    UserMenuRecommendationSerializer,
    UserMenuRecommendationDetailSerializer
)

# 1. 특정 메뉴에 대한 추천 추가
class CreateRecommendationView(generics.CreateAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 2. 특정 메뉴에 대한 추천/비추천 개수 조회 (로그인 없이 접근 가능)
class MenuRecommendationCountView(generics.RetrieveAPIView):
    serializer_class = MenuRecommendationCountSerializer
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        menu = self.get_object()
        true_count = Recommendation.objects.filter(menu=menu, recommendation=True).count()
        false_count = Recommendation.objects.filter(menu=menu, recommendation=False).count()

        data = {
            'menu_id': menu.id, 
            'true_count': true_count,
            'false_count': false_count,
            'date': menu.date,
            'restaurant': menu.restaurant.name  
        }
        serializer = MenuRecommendationCountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


# 3. 로그인한 유저가 입력한 모든 추천 메뉴 조회
class UserRecommendationsView(generics.ListAPIView):
    serializer_class = UserMenuRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Recommendation.objects.filter(user=user)

# 4. 로그인한 유저가 특정 메뉴에 대한 추천 수정
class UpdateRecommendationView(generics.UpdateAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        menu_id = self.kwargs.get('menu_id')
        try:
            recommendation = Recommendation.objects.get(user=user, menu_id=menu_id)
        except Recommendation.DoesNotExist:
            raise NotFound("해당 메뉴에 대한 추천이 존재하지 않습니다.")
        return recommendation

# 5. 로그인한 유저가 특정 메뉴에 대한 추천 삭제
class DeleteRecommendationView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        menu_id = self.kwargs.get('menu_id')
        try:
            recommendation = Recommendation.objects.get(user=user, menu_id=menu_id)
        except Recommendation.DoesNotExist:
            raise NotFound("해당 메뉴에 대한 추천이 존재하지 않습니다.")
        return recommendation

# 6. 로그인 한 유저가 특정 메뉴에 대한 정보와 추천 여부 출력    
class UserMenuRecommendationDetailView(generics.RetrieveAPIView):
    serializer_class = UserMenuRecommendationDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        menu_id = self.kwargs.get('menu_id')

        try:
            menu = Menu.objects.get(id=menu_id)
            # 사용자가 해당 메뉴에 대한 추천을 했는지 확인
            recommendation = Recommendation.objects.get(user=user, menu=menu)
            return menu, recommendation
        except Menu.DoesNotExist:
            raise NotFound("해당 메뉴를 찾을 수 없습니다.")
        except Recommendation.DoesNotExist:
            return menu, None  # 사용자가 추천하지 않았을 경우

    def retrieve(self, request, *args, **kwargs):
        menu, recommendation = self.get_object()
        serializer = self.get_serializer(menu)

        # 응답 데이터에 추천 정보를 포함
        response_data = serializer.data
        response_data['recommendation'] = recommendation.recommendation if recommendation else None

        return Response(response_data)
