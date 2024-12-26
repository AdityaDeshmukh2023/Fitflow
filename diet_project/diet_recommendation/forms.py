# diet_recommendation/forms.py
from django import forms
from .models import UserProfile

class DietRecommendationForm(forms.ModelForm):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    DIET_CHOICES = [('Veg', 'Veg'), ('Non-Veg', 'Non-Veg'), ('Veg & Non-Veg', 'Veg & Non-Veg')]
    GOAL_CHOICES = [
        ('Lose weight', 'Lose weight'),
        ('Gain weight', 'Gain weight'),
        ('Maintain physique', 'Maintain physique'),
        ('Gain muscles', 'Gain muscles'),
        ('Endurance Training', 'Endurance Training'),
        ('Improved Energy Levels', 'Improved Energy Levels'),
        ('Boost Immunity', 'Boost Immunity'),
        ('Improve Gut Health', 'Improve Gut Health'),
    ]
    Activity_Level = [('Sedentary', 'Sedentary'), ('moderately active', 'moderately active'), ('active', 'active')]
    Target_timeline = [('1 month', '1 month'), ('3 months', '3 months'), ('6 months', '6 months'), ('1 year', '1 year')]
    # LANGUAGE_CHOICES = [
    #     ("English", "English"), ("Hindi", "Hindi"), ("Bengali", "Bengali"),
    #     ("Punjabi", "Punjabi"), ("Tamil", "Tamil"), ("Telugu", "Telugu"),
    #     ("Urdu", "Urdu"), ("Spanish", "Spanish"), ("French", "French"),
    #     ("German", "German")
    # ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    Food_type = forms.ChoiceField(choices=DIET_CHOICES)
    goal = forms.ChoiceField(choices=GOAL_CHOICES)
    Activity_level = forms.ChoiceField(choices=Activity_Level)
    Target_timeline = forms.ChoiceField(choices=Target_timeline)
    # language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = UserProfile
        exclude = ['created_at']
        widgets = {
            'disease': forms.Textarea(attrs={'rows': 3}),
            'allergics': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
            })