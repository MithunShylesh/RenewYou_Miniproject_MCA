from django import forms
from .models import*
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['username', 'created_at']
        widgets = {
            'allergies': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control textarea-small'
            }),
            'medical_conditions': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control textarea-large'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
         if field.widget.__class__.__name__ == 'Select':
            field.widget.attrs['class'] = 'form-select'
         else:
            field.widget.attrs['class'] = 'form-control'





class userregistrationform(forms.ModelForm):
    class Meta:
        model=userregistration
        fields='__all__'

class FoodRecommendationForm(forms.Form):

    PURPOSE_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('immunity', 'Immunity Boost'),
        ('general', 'General Health'),
    ]

    MEAL_TIME_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('pre_workout', 'Pre Workout'),
        ('post_workout', 'Post Workout'),
    ]

    FOOD_TYPE_CHOICES = [
        ('juice', 'Juice'),
        ('light', 'Light Food'),
        ('heavy', 'Heavy Food'),
    ]

    DIET_CHOICES = [
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegetarian'),
    ]

    HEALTH_CONDITION_CHOICES = [
        ('none', 'None'),
        ('diabetes', 'Diabetes'),
        ('bp', 'High Blood Pressure'),
        ('thyroid', 'Thyroid'),
        ('pcos', 'PCOS'),
        ('cholesterol', 'Cholesterol'),
    ]

    CALORIE_CHOICES = [
        ('low', 'Low Calorie (<300 kcal)'),
        ('moderate', 'Moderate (300–500 kcal)'),
        ('high', 'High Calorie (>500 kcal)'),
    ]

    CUISINE_CHOICES = [
        ('south_indian', 'South Indian'),
        ('north_indian', 'North Indian'),
        ('kerala', 'Kerala Style'),
        ('continental', 'Continental'),
        ('mediterranean', 'Mediterranean'),
    ]

    SPICE_CHOICES = [
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('spicy', 'Spicy'),
    ]

    PREP_TIME_CHOICES = [
        ('quick', 'Under 15 mins'),
        ('medium', '15-30 mins'),
        ('long', '30+ mins'),
    ]

    purpose = forms.ChoiceField(choices=PURPOSE_CHOICES)
    meal_time = forms.ChoiceField(choices=MEAL_TIME_CHOICES)
    food_type = forms.ChoiceField(choices=FOOD_TYPE_CHOICES)
    diet_type = forms.ChoiceField(choices=DIET_CHOICES)
    health_condition = forms.ChoiceField(choices=HEALTH_CONDITION_CHOICES)
    calorie_target = forms.ChoiceField(choices=CALORIE_CHOICES)
    cuisine = forms.ChoiceField(choices=CUISINE_CHOICES)
    spice_level = forms.ChoiceField(choices=SPICE_CHOICES)
    preparation_time = forms.ChoiceField(choices=PREP_TIME_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select text-center'
