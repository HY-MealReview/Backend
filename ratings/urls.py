from django.urls import path
from .views import (
    RatingCreateView, RatingUpdateView, RatingDeleteView,
    FoodRatingSummaryView, UserFoodRatingsView, UserRatingDetailView,
)

urlpatterns = [
    path('rating/', RatingCreateView.as_view(), name='rating-create'),
    path('rating/<int:pk>/update/', RatingUpdateView.as_view(), name='rating-update'),
    path('rating/<int:food_id>/delete/', RatingDeleteView.as_view(), name='rating-delete'),
    path('rating/user/all/', UserFoodRatingsView.as_view(), name='user-food-ratings'),
    path('rating/user/food/<int:pk>/', UserRatingDetailView.as_view(), name='user-rating-detail'),
    path('rating/food/<int:pk>/average/', FoodRatingSummaryView.as_view(), name='food-rating-summary'),
]