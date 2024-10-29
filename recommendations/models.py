from django.db import models
from django.db.models import UniqueConstraint

class Recommendation(models.Model):
    menu = models.ForeignKey('restaurants.Menu', on_delete=models.CASCADE, related_name='recommendations')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='recommendations')
    recommendation = models.BooleanField()

    # menu와 user가 동시에 중복 방지
    class Meta:
        constraints = [
            UniqueConstraint(fields=['menu', 'user'], name='unique_user_menu_recommendation')
        ]

    def __str__(self):
        return f"{self.menu.date}의 {self.menu.restaurant.name} 메뉴에 대한 {self.user.nickname}님의 추천"
