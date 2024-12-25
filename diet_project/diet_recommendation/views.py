# diet_recommendation/views.py
from django.shortcuts import render
from .forms import DietRecommendationForm
from .models import UserProfile, DietRecommendation  # Add this import
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def calculate_bmi(weight, height):
    height_m = height / 100.0
    bmi = weight / (height_m ** 2)
    
    if bmi < 18.5:
        category = 'Underweight'
    elif 18.5 <= bmi < 24.9:
        category = 'Normal weight'
    elif 25 <= bmi < 29.9:
        category = 'Overweight'
    else:
        category = 'Obesity'
    
    return bmi, category

def diet_recommendation_view(request):
    if request.method == 'POST':
        form = DietRecommendationForm(request.POST)
        if form.is_valid():
            profile = form.save()
            
            # Calculate BMI
            bmi, bmi_category = calculate_bmi(float(profile.weight), float(profile.height))
            
            # Configure the API key
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            
            # Create the model
            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""
            Personalized Diet and Wellness Plan:
            Based on the following information, provide a detailed and personalized daily meal plan along with suitable fitness recommendations:
            - Age: {profile.age}
            - Gender: {profile.gender}
            - Weight: {profile.weight} kg
            - Height: {profile.height} cm
            - Dietary Preference: {profile.veg_or_nonveg}
            - Goal: {profile.goal}
            - Health Conditions: {profile.disease}
            - Country: {profile.country}
            - State/Province: {profile.state}
            - Food Allergies: {profile.allergics}
            - Preferred Food Type: {profile.food_type}
            
            Output Language: {profile.language}

            Recommendations should include:
            1. A balanced breakfast, lunch, and dinner plan
            2. 3 healthy snack options
            3. Essential nutrients and foods to include/avoid
            4. Workout suggestions aligned with their goals
            5. Lifestyle tips for overall wellness
            """

            response = model.generate_content(prompt)
            recommendation_text = response.text

            # Save recommendation
            diet_recommendation = DietRecommendation.objects.create(
                profile=profile,
                recommendation_text=recommendation_text,
                bmi=bmi,
                bmi_category=bmi_category
            )

            return render(request, 'diet/recommendation_result.html', {
                'recommendation': recommendation_text,
                'bmi': bmi,
                'bmi_category': bmi_category,
                'profile': profile
            })
    else:
        form = DietRecommendationForm()

    return render(request, 'diet/recommendation_form.html', {'form': form})