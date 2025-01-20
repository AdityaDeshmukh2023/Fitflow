from rest_framework import serializers
from .models import UserProfile, DietRecommendation
import json

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class DietRecommendationSerializer(serializers.ModelSerializer):
    recommendation_text = serializers.SerializerMethodField()

    class Meta:
        model = DietRecommendation
        fields = '__all__'

    def get_recommendation_text(self, obj):
        try:
            return json.loads(obj.recommendation_text)
        except:
            return obj.recommendation_text