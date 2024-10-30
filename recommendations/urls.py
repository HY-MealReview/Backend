from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.CreateRecommendationView.as_view(), name='create-recommendation'),
    path('recommend/<int:menu_id>/update/', views.UpdateRecommendationView.as_view(), name='update-recommendation'),
    path('recommend/<int:menu_id>/delete/', views.DeleteRecommendationView.as_view(), name='delete-recommendation'),
    path('recommend/<int:menu_id>/', views.UserMenuRecommendationDetailView.as_view(), name='user-menu-recommendation-detail'),
    path('recommend/user/', views.UserRecommendationsView.as_view(), name='user-recommendations'),
    path('recommend/menu/<int:pk>/count/', views.MenuRecommendationCountView.as_view(), name='menu-recommendation-count'),
]
