from django.urls import path
from .views import (
    RestaurantCreateView, RestaurantUpdateView, RestaurantDeleteView, RestaurantListView,
    MenuCreateView, MenuUpdateView, MenuDeleteView, MenuListView,
    MenuDetailView, MenuAddFoodView,
)

urlpatterns = [
    path('restaurant/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('restaurant/<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant-update'),
    path('restaurant/<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant-delete'),
    path('restaurant/all/', RestaurantListView.as_view(), name='restaurant-list'),
    
    path('menu/', MenuCreateView.as_view(), name='menu-create'),
    path('menu/<int:pk>/update/', MenuUpdateView.as_view(), name='menu-update'),
    path('menu/<int:pk>/delete/', MenuDeleteView.as_view(), name='menu-delete'),
    path('menu/all/', MenuListView.as_view(), name='menu-list'),

    path('menu/detail/', MenuDetailView.as_view(), name='menu-detail'),  # restaurant와 date는 query_params로 받음
    path('menu/<int:pk>/addfood/', MenuAddFoodView.as_view(), name='menu-add-food'),
]


# /menu/detail/?restaurant=레스토랑이름&date=YYYY-MM-DD
# 예시) GET /menu/detail/?restaurant=PizzaPlace&date=2024-10-28
