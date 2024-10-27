# foods/urls.py
from django.urls import path
from .views import CategoryCreateView, FoodCreateView

urlpatterns = [
    path('categories/', CategoryCreateView.as_view(), name='category-create'),
    path('foods/', FoodCreateView.as_view(), name='food-create'),
]
