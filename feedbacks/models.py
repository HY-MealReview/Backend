from django.db import models

class Feedback(models.Model) :
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='feedback')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback by {self.user.nickname} - {self.content[:20]}"
