# restaurants/urls.py
from django.urls import path
from .views import RestaurantCreateView, MenuCreateView, MenuDetailView

urlpatterns = [
    path('restaurants/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('menus/', MenuCreateView.as_view(), name='menu-create'),
    path('menu-details/', MenuDetailView.as_view(), name='menu-detail'),
]

# /menu-details/?restaurant=레스토랑이름&date=YYYY-MM-DD
# 예시) GET /menu-details/?restaurant=PizzaPlace&date=2024-10-28
