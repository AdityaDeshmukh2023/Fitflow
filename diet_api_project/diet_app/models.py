from django.db import models

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    FOOD_TYPE_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NVEG', 'Non-Vegetarian'),
        ('VEGAN', 'Vegan')
    ]
    
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.FloatField()
    height = models.FloatField()
    Food_type = models.CharField(max_length=5, choices=FOOD_TYPE_CHOICES)
    goal = models.CharField(max_length=200)
    disease = models.TextField(blank=True)
    allergics = models.TextField(blank=True)
    Target_timeline = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class DietRecommendation(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recommendation_text = models.TextField()
    bmi = models.FloatField()
    bmi_category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)