from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
class userregistration(models.Model):
    name=models.CharField(max_length=20)
    ph_no = models.CharField(max_length=15)

    # address=models.CharField(max_length=100)
    email=models.EmailField()
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)

    # Basic
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[('male','Male'), ('female','Female'), ('other','Other')]
    )
    height = models.FloatField(help_text="cm")
    weight = models.FloatField(help_text="kg")
    target_weight = models.FloatField(null=True, blank=True)

    # Job & Activity
    job_type = models.CharField(max_length=50)
    work_nature = models.CharField(
        max_length=20,
        choices=[('desk','Desk'), ('field','Field'), ('mixed','Mixed')]
    )
    activity_level = models.CharField(
        max_length=20,
        choices=[
            ('low','Low'),
            ('moderate','Moderate'),
            ('high','High')
        ]
    )

    # Mental & Social
    stress_level = models.CharField(
        max_length=20,
        choices=[
            ('low','Low'),
            ('medium','Medium'),
            ('high','High')
        ]
    )
    sleep_hours = models.FloatField()
    personality = models.CharField(
        max_length=20,
        choices=[
            ('introvert','Introvert'),
            ('extrovert','Extrovert'),
            ('ambivert','Ambivert')
        ]
    )

    # Habits
    smoking = models.CharField(
    max_length=10,
    choices=[
        ('', 'Choose'),
        ('yes', 'Yes'),
        ('no', 'No')
    ],
    blank=True
)
  
    alcohol = models.CharField(
        max_length=20,
        choices=[
            ('never','Never'),
            ('occasional','Occasional'),
            ('regular','Regular')
        ]
    )
    water_intake = models.FloatField(help_text="Liters per day")

    # Food & Health
    food_preference = models.CharField(
        max_length=20,
        choices=[('veg','Vegetarian'), ('nonveg','Non-Vegetarian'), ('vegan','Vegan')]
    )
    meals_per_day = models.IntegerField()
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    health_goal = models.CharField(
        max_length=30,
        choices=[
            ('weight_loss','Weight Loss'),
            ('weight_gain','Weight Gain'),
            ('muscle_gain','Muscle Gain'),
            ('general','General Health')
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
from django.contrib.auth.models import User

class FoodRecommendation(models.Model):
    PURPOSE_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('immunity', 'Immunity Boost'),
        ('general', 'General Health'),
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

    user = models.ForeignKey(userregistration, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES)
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES)
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.purpose}"
from django.utils import timezone
from datetime import timedelta




class TrackingPlan(models.Model):
    user = models.ForeignKey(userregistration, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)
    reset_count = models.IntegerField(default=0) 

    def end_date(self):
        return self.start_date + timedelta(days=self.duration_days)

    def __str__(self):
        return f"{self.user.username} - {self.duration_days} days"


class DailyTracking(models.Model):
    plan = models.ForeignKey(TrackingPlan, on_delete=models.CASCADE)
    date = models.DateField()
    diet_followed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('plan', 'date')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.plan.user.username} - {self.date}"
    
class Tracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day1 = models.BooleanField(default=False)
    day2 = models.BooleanField(default=False)

    reset_count = models.IntegerField(default=0)  # ✅ ADD THIS
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


