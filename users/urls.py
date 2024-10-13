from django.urls import path
from .views import UserRegistrationView, UserDetailView, ChangePasswordView, ChangeNicknameView

urlpatterns = [
    path('users/', UserRegistrationView.as_view(), name='register'),
    path('users/detail', UserDetailView.as_view(), name='user_detail'),
    path('users/change/password', ChangePasswordView.as_view(), name='change_password'),
    path('users/change/nickname', ChangeNicknameView.as_view(), name='change_nickname'),
]
