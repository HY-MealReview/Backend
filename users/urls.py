from django.urls import path
from .views import UserRegistrationView, UserDetailView, ChangePasswordView, ChangeNicknameView, UserListView, UserDeleteView, StudentIDCheckView, NicknameCheckView

urlpatterns = [
    path('users/', UserRegistrationView.as_view(), name='register'),
    path('users/detail/', UserDetailView.as_view(), name='user_detail'),
    path('users/all/', UserListView.as_view(), name='user_list'),
    path('users/change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/change/nickname/', ChangeNicknameView.as_view(), name='change_nickname'),
    path('users/delete/', UserDeleteView.as_view(), name='user_delete'),  # 사용자 탈퇴

    path('users/check/studentid/', StudentIDCheckView.as_view(), name='check-student-id'),
    path('users/check/nickname/', NicknameCheckView.as_view(), name='check-nickname'),
]
