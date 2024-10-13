from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import update_session_auth_hash

from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# 사용자 등록 (회원가입)
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # 누구나 접근 가능

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인한 사용자의 정보 조회
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "student_id": user.student_id,
            "nickname": user.nickname,
        }, status=status.HTTP_200_OK)
    
# 전체 사용자 정보 조회
class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]  # 관리자만 접근 가능

    def get(self, request):
        users = User.objects.all()
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data)

# 로그인한 사용자의 비밀번호 변경
class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # 기존 비밀번호가 맞는지 확인
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # 새 비밀번호 설정
        user.set_password(new_password)
        user.save()

        # 비밀번호 변경 후 세션 유지
        update_session_auth_hash(request, user)

        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

# 로그인한 사용자의 닉네임 변경
class ChangeNicknameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        user = request.user
        new_nickname = request.data.get('nickname')

        if not new_nickname:
            return Response({"error": "Nickname is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 닉네임 변경
        user.nickname = new_nickname
        user.save()

        return Response({"message": "Nickname changed successfully"}, status=status.HTTP_200_OK)
    
# 로그인한 사용자의 탈퇴
class UserDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def delete(self, request):
        user = request.user  # 요청한 사용자
        user.delete()  # 사용자 삭제
        return Response({"message": "User account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
