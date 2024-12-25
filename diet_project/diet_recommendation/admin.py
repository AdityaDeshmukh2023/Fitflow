
from django.contrib import admin
from .models import UserProfile, DietRecommendation

admin.site.register(UserProfile)
admin.site.register(DietRecommendation)