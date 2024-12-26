# diet_recommendation/models.py
from django.db import models

class UserProfile(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    Food_type = models.CharField(max_length=20, default='Not Specified')
    goal = models.CharField(max_length=50)
    disease = models.TextField(blank=True)
    # country = models.CharField(max_length=100)
   
    allergics = models.TextField(blank=True)
    Activity_level = models.CharField(max_length=100)
    # language = models.CharField(max_length=20) 
    Target_timeline = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class DietRecommendation(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recommendation_text = models.TextField()
    bmi = models.FloatField()
    bmi_category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    