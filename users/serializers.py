# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# 1. 사용자 등록 (ModelSerializer 사용)
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

# 2. 사용자 로그인 (Serializer 사용)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    student_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        student_id = attrs.get("student_id")
        password = attrs.get("password")

        if student_id and password:
            user = authenticate(student_id=student_id, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Both fields are required")

        return super().validate(attrs)
