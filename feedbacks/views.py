from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackCreateUpdateSerializer

# 1. 피드백 생성
class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 2. 피드백 수정
class FeedbackUpdateView(generics.UpdateAPIView):
    serializer_class = FeedbackCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

# 3. 피드백 삭제
class FeedbackDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

# 4. 로그인 한 user가 작성한 모든 피드백 춮력
class FeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

# 5. 모든 user 들의 feedback 출력 (관리자 계정만 가능)
class FeedbackAllListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Feedback.objects.all()