from django.urls import path
from .views import (
    FeedbackCreateView, FeedbackListView, FeedbackAllListView,
    FeedbackUpdateView, FeedbackDeleteView,
)

urlpatterns = [
    path('feedback/create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback/<int:pk>/update/', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('feedback/<int:pk>/delete/', FeedbackDeleteView.as_view(), name='feedback-delete'),
    path('feedback/mine/', FeedbackListView.as_view(), name='my-feedbacks'),
    path('feedback/all/', FeedbackAllListView.as_view(), name='all-feedbacks'),
]
