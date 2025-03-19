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
    bmi = weight / (height_m**2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"

    return bmi, category


def diet_recommendation_view(request):
    if request.method == "POST":
        form = DietRecommendationForm(request.POST)
        if form.is_valid():
            profile = form.save()

            # Calculate BMI
            bmi, bmi_category = calculate_bmi(
                float(profile.weight), float(profile.height)
            )

            # Configure the API key
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

            # Create the model
            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""
            As an expert fitness trainer, create a comprehensive, personalized fitness plan in valid JSON format following this exact structure:

            {{
                "user_profile": {{
                    "personal_info": {{
                        "age": {profile.age},
                        "gender": "{profile.gender}",
                        "current_weight": {profile.weight},
                        "height": {profile.height},
                        "health_goal": "{profile.goal}",
                        "medical_conditions": "{profile.disease}",
                        "physical_limitations": "{profile.injuries_or_physical_limitation}",
                        "fitness_level": "{profile.fitness_level}",
                        "activity_level": "{profile.Activity_level}",
                        "target_timeline": "{profile.Target_timeline}",
                        "exercise_setting": "{profile.exercise_setting}",
                        "sleep_pattern": "{profile.sleep_pattern}",
                        "focus_areas": "{profile.Specific_area}"
                    }},
                    
                    "fitness_assessment": {{
                        "bmi": "calculated_value",
                        "bmi_category": "category",
                        "recommended_heart_rate_zones": {{
                            "low_intensity": "range",
                            "moderate_intensity": "range",
                            "high_intensity": "range"
                        }},
                        "current_limitations": []
                    }}
                }},

                "workout_plan": {{
                    "weekly_schedule": [
                        {{
                            "day": "1",
                            "focus": "area_of_focus",
                            "workout_type": "type",
                            "duration": "minutes",
                            "intensity": "level",
                            "exercises": [
                                {{
                                    "name": "exercise_name",
                                    "sets": "number",
                                    "reps": "number",
                                    "rest": "seconds",
                                    "notes": "special_instructions",
                                    "alternatives": ["option1", "option2"],
                                    "video_reference": "url"
                                }}
                            ],
                            "warmup": [],
                            "cooldown": []
                        }}
                    ],
                    
                    "progression_plan": {{
                        "week1_to_2": {{
                            "volume_increase": "percentage",
                            "intensity_increase": "percentage",
                            "new_exercises": []
                        }},
                        "week3_to_4": {{
                            "volume_increase": "percentage",
                            "intensity_increase": "percentage",
                            "new_exercises": []
                        }}
                    }}
                }},

                "recovery_plan": {{
                    "rest_days": {{
                        "frequency": "number_per_week",
                        "recommended_activities": []
                    }},
                    "sleep_recommendations": {{
                        "recommended_hours": "number",
                        "sleep_schedule": {{
                            "bedtime": "time",
                            "wake_time": "time"
                        }},
                        "sleep_optimization_tips": []
                    }},
                    "mobility_work": {{
                        "frequency": "times_per_week",
                        "duration": "minutes",
                        "recommended_exercises": []
                    }}
                }},

                "safety_guidelines": {{
                    "medical_considerations": [],
                    "form_tips": [],
                    "warning_signs": [],
                    "modification_guidelines": []
                }},

                "progress_tracking": {{
                    "metrics_to_track": [],
                    "measurement_frequency": {{
                        "weight": "frequency",
                        "measurements": "frequency",
                        "progress_photos": "frequency",
                        "strength_tests": "frequency"
                    }},
                    "milestones": [
                        {{
                            "timeline": "week_number",
                            "expected_progress": "description",
                            "metrics": {{}}
                        }}
                    ]
                }},

                "equipment_needed": {{
                    "essential": [],
                    "optional": [],
                    "alternatives": {{}}
                }}
            }}

            Generate a personalized fitness plan that:
            1. Accounts for the age ({profile.age}) and gender ({profile.gender})
            2. Considers medical conditions: {profile.disease}
            3. Adapts for injuries/limitations: {profile.injuries_or_physical_limitation}
            4. Matches fitness level: {profile.fitness_level}
            5. Aligns with activity level: {profile.Activity_level}
            6. Focuses on target areas: {profile.Specific_area}
            7. Provides progression for: {profile.Target_timeline}
            8. Works with available setting: {profile.exercise_setting}
            9. Accounts for sleep pattern: {profile.sleep_pattern}

            Ensure the plan:
            - Includes detailed exercise descriptions
            - Provides alternative exercises for each movement
            - Includes proper warm-up and cool-down routines
            - Addresses any medical conditions or injuries
            - Gives clear progression guidelines
            - Includes safety precautions
            - Matches the user's available equipment
            - Provides modifications for different fitness levels
            - Includes recovery protocols
            - Has clear tracking metrics

            The exercises should be:
            1. Appropriate for the user's fitness level
            2. Achievable in the specified setting
            3. Safe considering any medical conditions
            4. Progressive over the timeline
            5. Focused on the specified target areas
            6. Balanced to prevent overuse injuries
            7. Adaptable based on available equipment

            Return ONLY the JSON response without any additional text or markdown formatting.
            """

            # response = model.generate_content(prompt)
            # recommendation_text = response.text

            response = model.generate_content(prompt)
            # In views.py
            recommendation_text = (
                response.text.replace("*", "").replace("#", "").replace("```", "")
            )

            # Save recommendation
            diet_recommendation = DietRecommendation.objects.create(
                profile=profile,
                recommendation_text=recommendation_text,
                bmi=bmi,
                bmi_category=bmi_category,
            )

            return render(
                request,
                "diet/recommendation_result.html",
                {
                    "recommendation": recommendation_text,
                    "bmi": bmi,
                    "bmi_category": bmi_category,
                    "profile": profile,
                },
            )
    else:
        form = DietRecommendationForm()

    return render(request, "diet/recommendation_form.html", {"form": form})
