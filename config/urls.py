from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT 토큰 발급
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 리프레시 토큰으로 새로운 액세스 토큰 발급
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('users.urls')),
    path('', include('restaurants.urls')),
    path('', include('foods.urls')),
    path('', include('recommendations.urls')),
    path('', include('ratings.urls')),
    path('', include('feedbacks.urls'))
]

# 미디어 파일 제공 설정 추가 (DEBUG 모드에서만)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)