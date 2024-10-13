from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['student_id', 'nickname', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            student_id=validated_data['student_id'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        return user
