from django.db import models

class Rating(models.Model):
    food = models.ForeignKey('foods.Food', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'food'], name='unique_user_food_rating'),  # user와 food의 조합이 유일해야 함
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=10),
                name='rating_between_1_and_10'
            )
        ]

    def __str__(self):
        return f"{self.user.nickname} rated {self.food.name} with {self.rating}"