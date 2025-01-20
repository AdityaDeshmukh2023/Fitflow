from rest_framework import serializers
from .models import UserProfile, DietRecommendation

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['created_at']

class DietRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietRecommendation
        fields = ['recommendation_text', 'bmi', 'bmi_category']