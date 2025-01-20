from django.urls import path
from .views import DietRecommendationAPI

urlpatterns = [
    path('diet-recommendation/', DietRecommendationAPI.as_view(), name='diet-recommendation'),
]