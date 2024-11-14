from django.db import models

class Rating(models.Model):
    food = models.ForeignKey('foods.Food', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜 추가

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'food'], name='unique_user_food_rating'),
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=10),
                name='rating_between_1_and_10'
            )
        ]

    def __str__(self):
        return f"{self.user.nickname} rated {self.food.name} with {self.rating}"
