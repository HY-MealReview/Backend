from rest_framework import generics, permissions
from .models import Rating
from .serializers import RatingSerializer, FoodRatingSummarySerializer, UserFoodRatingsSerializer
from foods.models import Food

# 1. 로그인된 사용자가 특정 food의 rating 입력
class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

# 2. 로그인된 사용자가 입력한 특정 food의 rating 수정
class RatingUpdateView(generics.UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

# 3. 로그인된 사용자가 입력한 특정 food의 rating 삭제
class RatingDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'food_id' 

    def get_queryset(self):
        food_id = self.kwargs.get('food_id') 
        return Rating.objects.filter(user=self.request.user, food_id=food_id)

    def perform_destroy(self, instance):
        instance.delete()  

# 4. 로그인된 사용자가 입력한 rating들이 해당되는 food의 정보와 rating 전체 출력
class UserFoodRatingsView(generics.ListAPIView):
    serializer_class = UserFoodRatingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Food.objects.filter(ratings__user=user).distinct()

# 5. 로그인된 사용자가 특정 food의 id를 입력하면 해당하는 rating 출력
class UserRatingDetailView(generics.RetrieveAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Rating.objects.filter(user=user)

# 6. 특정 food의 id를 입력하면 해당 food에 입력된 모든 user들의 rating의 합계 및 평균 출력 (로그인 필요 없음)
class FoodRatingSummaryView(generics.RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodRatingSummarySerializer