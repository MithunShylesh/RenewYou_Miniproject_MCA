import re
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*
from .forms import*
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def index(request):
    return render(request,'user/index.html')
def healthcare_tips(request):
    return render(request,'user/healthcare_tips.html')
def registration(request):
    if request.method == "POST":
        name = request.POST['name']
        ph_no = request.POST['ph_no']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # check username exists
        if userregistration.objects.filter(username__iexact=username).exists():
            return render(request, 'user/registration.html', {
                    "error": "Username already exists. Please login instead."
                })


        if password != confirm_password:
            return render(request, 'user/registration.html', {
                    "error": "Passwords do not match"
                })


        userregistration.objects.create(
            name=name,
            ph_no=ph_no,
            email=email,
            username=username,
            password=password
        )

        return render(request, 'user/registration.html', {
            "success": "Registration successful! Please login."
        })


    return render(request, 'user/registration.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # USER LOGIN
        try:
            user = userregistration.objects.get(username__iexact=username)

            if user.password == password:
                request.session['user'] = user.username
                return redirect('userprofile')
            else:
                return render(request, 'user/login.html', {
                    "error": "Incorrect username or password"
                })


        except userregistration.DoesNotExist:
            pass  # move to admin check

        # ADMIN LOGIN (HARDCODED)
        if username == 'Renewyou' and password == 'Admin@1234':
            request.session['admin'] = username
            return redirect('adminhome')

        return render(request, 'user/login.html', {
                    "error": "Incorrect username or password"
                })


    return render(request, 'user/login.html')



def userprofile(request):
    username = request.session.get('user')

    if not username:
        return redirect('login')

    try:
        profile = UserProfile.objects.get(username=username)
        profile_exists = True
    except ObjectDoesNotExist:
        profile = None
        profile_exists = False

    if request.method == "POST":
        if profile_exists:
            form = UserProfileForm(request.POST, instance=profile)
        else:
            form = UserProfileForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = username
            obj.save()
            messages.success(request, "✅ Your health profile has been saved successfully!")
            return redirect('userprofile')

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'userweb/userprofile.html', {
        'form': form,
        'profile_exists': profile_exists
    })


from .ai_nutrition import generate_nutrition_plan

def personalised_nutrition(request):
    username = request.session.get('user')

    if not username:
        return redirect('login')

    try:
        profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return render(request, 'userweb/personalised_nutrition.html', {
            'profile_complete': False
        })

    # CHECK REQUIRED FIELDS
    required_fields = [
        profile.age,
        profile.height,
        profile.weight,
        profile.activity_level,
        profile.food_preference,
        profile.health_goal
    ]

    if not all(required_fields):
        return render(request, 'userweb/personalised_nutrition.html', {
            'profile_complete': False
        })

    # AI PLAN GENERATION
    plan = generate_nutrition_plan(profile)

    return render(request, 'userweb/personalised_nutrition.html', {
        'profile_complete': True,
        'profile': profile,
        'plan': plan
    })
from django.shortcuts import render
from .forms import FoodRecommendationForm
from .ai_nutrition import generate_food_recommendation
from .models import FoodRecommendation

def food_recommendation_view(request):

    recommendation = None

    if request.method == 'POST':
        form = FoodRecommendationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Generate AI Recommendation
            recommendation = generate_food_recommendation(
                data['purpose'],
                data['meal_time'],
                data['food_type'],
                data['diet_type'],
                data['health_condition'],
                data['calorie_target'],
                data['cuisine'],
                data['spice_level'],
                data['preparation_time']
            )

            # Save to database (if authenticated)
            username = request.session.get('user')
            if username:
                user = userregistration.objects.get(username=username)
                FoodRecommendation.objects.create(
                user=user,
                purpose=data['purpose'],
                food_type=data['food_type'],
                diet_type=data['diet_type'],
                recommendation=recommendation)

    else:
        form = FoodRecommendationForm()

    return render(request, 'userweb/food_recommendation.html', {
        'form': form,
        'recommendation': recommendation
    })
from datetime import timedelta
from django.shortcuts import render, redirect
from .models import TrackingPlan, DailyTracking, userregistration
from datetime import date
from .models import UserProfile

def tracking_dashboard(request):

    username = request.session.get("user")
    if not username:
        return redirect("login")

    user = userregistration.objects.get(username=username)
    last_plan = TrackingPlan.objects.filter(user=user).order_by('-id').first()
    reset_count = last_plan.reset_count if last_plan else 0

    # Check profile exists
    profile_complete = UserProfile.objects.filter(username=username).exists()

    plan = TrackingPlan.objects.filter(user=user, is_active=True).first()

    # If no plan → show start form
    if not plan:
        return render(request, "userweb/tracking.html", {
            "profile_complete": profile_complete,
            "plan": None,
            "day_range": range(30, 101),
            "reset_count": reset_count
        })

    # If plan exists → build daily tracking objects
    daily_objects = []

    for i in range(plan.duration_days):
        current_date = plan.start_date + timedelta(days=i)

        daily, created = DailyTracking.objects.get_or_create(
            plan=plan,
            date=current_date
        )

        # Allow tick only for today or past
        daily.can_tick = daily.date <= date.today()

        daily_objects.append(daily)

    total_days = plan.duration_days
    completed_days = sum(1 for d in daily_objects if d.diet_followed)
    completion_rate = (completed_days / total_days) * 100 if total_days > 0 else 0
    last_plan = TrackingPlan.objects.filter(user=user).order_by('-id').first()
    reset_count = last_plan.reset_count if last_plan else 0

    return render(request, "userweb/tracking.html", {
        "profile_complete": profile_complete,
        "plan": plan,   # ✅ IMPORTANT FIX
        "daily_objects": daily_objects,
        "completion_rate": completion_rate,
         "reset_count": reset_count 
    })




def start_tracking(request):

    username = request.session.get('user')
    if not username:
        return redirect("login")

    if request.method != "POST":
        return redirect("tracking_dashboard")

    duration = int(request.POST.get("duration"))
    user = userregistration.objects.get(username=username)

    # 🔥 get last reset count
    last_plan = TrackingPlan.objects.filter(user=user).order_by('-id').first()
    last_count = last_plan.reset_count if last_plan else 0

    # deactivate old plan
    TrackingPlan.objects.filter(user=user, is_active=True).update(is_active=False)

    # ✅ create new plan with SAME count
    TrackingPlan.objects.create(
        user=user,
        duration_days=duration,
        reset_count=last_count
    )

    return redirect("tracking_dashboard")
def generate_tracking_review(compliance):

    if compliance >= 85:
        return "Excellent discipline! You are highly consistent and results will be visible soon."

    elif compliance >= 60:
        return "Good effort! Improve daily consistency for better transformation."

    else:
        return "Consistency is low. Try following your diet daily to see progress."
def mark_daily_tracking(request, daily_id):

    daily = DailyTracking.objects.get(id=daily_id)

    # Allow only if date <= today
    if daily.date <= date.today():
        daily.diet_followed = not daily.diet_followed
        daily.save()

    return redirect("tracking_dashboard")
def help(request):
    return render(request, 'userweb/help.html')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ai_chatbot import generate_chat_response

@csrf_exempt   # ✅ VERY IMPORTANT
def chatbot_api(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        message = data.get("message", "").lower()

        # ✅ KEYWORDS CHECK
        allowed_keywords = [
            "food", "diet", "nutrition", "calories", "protein",
            "workout", "exercise", "fitness", "health", "weight",
            "muscle", "fat", "meal"
        ]

        # ✅ VALIDATION
        if not any(word in message for word in allowed_keywords):
            return JsonResponse({
                "error": "Only questions related to food, nutrition, workout and health are accepted"
            })

        # ✅ NORMAL RESPONSE
        response = generate_chat_response(message)

        return JsonResponse({
            "response": response
        })
    
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')  # make sure login URL exists
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Tracking

def reset_tracking(request):

    username = request.session.get("user")
    if not username:
        return redirect("login")

    user = userregistration.objects.get(username=username)

    plan = TrackingPlan.objects.filter(user=user, is_active=True).first()

    if plan:
        # ✅ increase reset count
        plan.reset_count += 1
        plan.save()

        # ❌ remove daily tracking
        DailyTracking.objects.filter(plan=plan).delete()

        # ✅ deactivate instead of delete
        plan.is_active = False
        plan.save()

    return redirect("tracking_dashboard")
def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        try:
            user = userregistration.objects.get(username__iexact=username)

            if new_password != confirm_password:
                return render(request, "user/forgot_password.html", {
                    "error": "Passwords do not match"
                })

            # ✅ update password
            user.password = new_password
            user.save()

            return render(request, "user/login.html", {
                "success": "Password updated successfully! Please login."
            })

        except userregistration.DoesNotExist:
            return render(request, "user/forgot_password.html", {
                "error": "Username not found"
            })

    return render(request, "user/forgot_password.html")
def adminhome(request):
    # check admin login
    if not request.session.get("admin"):
        return redirect("login")

    users = userregistration.objects.all()
    profiles = UserProfile.objects.all()

    # combine user + profile
    user_data = []

    for user in users:
        profile = UserProfile.objects.filter(username=user.username).first()

        user_data.append({
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "phone": user.ph_no,

            # ✅ PROFILE DATA
            "age": profile.age if profile else "N/A",
            "height": profile.height if profile else "N/A",
            "weight": profile.weight if profile else "N/A",
            "goal": profile.health_goal if profile else "N/A",
            "activity": profile.activity_level if profile else "N/A",
            "food_pref": profile.food_preference if profile else "N/A",
        })

    return render(request, "user/adminhome.html", {
        "user_data": user_data
    })
def delete_user(request, user_id):
    if not request.session.get("admin"):
        return redirect("login")

    try:
        user = userregistration.objects.get(id=user_id)

        # delete profile also
        UserProfile.objects.filter(username=user.username).delete()

        user.delete()

    except:
        pass

    return redirect("adminhome")
def appointments(request):
    if not request.session.get("admin"):
        return redirect("login")

    data = Appointment.objects.all().order_by("-created_at")

    return render(request, "user/appointments.html", {
        "appointments": data
    })
from .models import Appointment
from django.contrib import messages


def book_appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        message = request.POST.get("message")

        # DEBUG PRINT (optional)
        print(name, email, phone, date, message)

        Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            date=date,
            message=message
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect("home") # ✅ BETTER UX

    return redirect("home")

