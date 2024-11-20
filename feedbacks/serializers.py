from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # For displaying user nickname

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']

class FeedbackCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['content']
