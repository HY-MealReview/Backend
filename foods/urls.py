from django.urls import path
from .views import (
    CategoryCreateView, FoodCreateView, CategoryListView, FoodListView,
    FoodByCategoryView, FoodDetailByNameAndRestaurantView,
    CategoryUpdateView, FoodUpdateView,
    CategoryDeleteView, FoodDeleteView
)

urlpatterns = [
    path('category/', CategoryCreateView.as_view(), name='category-create'),
    path('food/', FoodCreateView.as_view(), name='food-create'),
    path('category/all/', CategoryListView.as_view(), name='category-list'),
    path('food/all/', FoodListView.as_view(), name='food-list'),
    path('food/search/bycategory/', FoodByCategoryView.as_view(), name='food-by-category'),  # 특정 Category로 Food 검색
    path('food/search/bynamerest/', FoodDetailByNameAndRestaurantView.as_view(), name='food-detail-by-name-and-restaurant'),  # 특정 Food 정보 조회
    path('category/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),  # Category 수정
    path('food/<int:pk>/', FoodUpdateView.as_view(), name='food-update'),  # Food 수정
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),  # Category 삭제
    path('food/<int:pk>/delete/', FoodDeleteView.as_view(), name='food-delete'),  # Food 삭제
]

# 카테고리로 음식 검색 : /food/search/bycategory/?name=카테고리이름
# 음식 이름과 식당 이름으로 음식 검색 : /food/search/bynamerest/?food_name=음식이름&restaurant_name=식당이름
