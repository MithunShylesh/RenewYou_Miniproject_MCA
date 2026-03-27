import profile


def generate_nutrition_plan(profile):
    bmi = round(profile.weight / ((profile.height / 100) ** 2), 2)

    # ---------- BMI STATUS ----------
    if bmi < 18.5:
        bmi_status = "Underweight"
        bmi_advice = "You need gradual weight gain using nutritious calorie-dense foods."
    elif bmi <= 24.9:
        bmi_status = "Healthy"
        bmi_advice = "Your BMI is in a healthy range. Maintain consistency."
    else:
        bmi_status = "Overweight"
        bmi_advice = "Focus on fat loss, regular activity, and balanced meals."
     # ---------- CURRENT CALORIE REQUIREMENT ----------
    bmr = 24 * profile.weight

    if profile.activity_level == 'low':
        activity_multiplier = 1.2
    elif profile.activity_level == 'moderate':
        activity_multiplier = 1.5
    else:
        activity_multiplier = 1.75

    current_calories = round(bmr * activity_multiplier)

    # ---------- CALORIE DECISION BASED ON GOAL ----------
    if profile.health_goal == 'weight_gain':
        target_calories = current_calories + 300
        calorie_action = "increase"
        calorie_advice = (
             "You need to increase your calorie intake by eating nutrient-dense foods "
             "such as nuts, milk, banana, peanut butter, rice, and lentils."
        )

    elif profile.health_goal == 'weight_loss':
        target_calories = current_calories - 300
        calorie_action = "reduce"
        calorie_advice = (
        "You need to reduce your calorie intake by controlling portions, "
        "avoiding fried foods, sugary drinks, and focusing on vegetables, fruits, and fiber-rich foods."
        )

    else:
        target_calories = current_calories
        calorie_action = "maintain"
        calorie_advice = (
        "You need to maintain your current calorie intake by following balanced meals "
        "and regular physical activity."
        )


    # ---------- HEALTH OVERVIEW PARAGRAPH ----------
    health_overview = (
        "High protein helps repair muscles, improves metabolism, and keeps you full. "
        "Healthy carbohydrates provide long-lasting energy and support brain function. "
        "This plan avoids junk calories and focuses on nutrient-rich foods."
    )

    calorie_explanation = (
        "A calorie surplus means adding calories using healthy foods like nuts, milk, "
        "banana, rice, and lentils — not junk food. A calorie deficit focuses on portion "
        "control and fiber-rich foods."
    )

    # ---------- WEEKLY MEAL PLAN ----------
    weekly_meals = {
        "Day 1": {
            "breakfast": "Vegetable oats – improves digestion",
            "lunch": "Brown rice + dal – sustained energy",
            "dinner": "Chapati + vegetables – light and nutritious"
        },
        "Day 2": {
            "breakfast": "Fruit smoothie – vitamins & hydration",
            "lunch": "Quinoa + vegetables – protein & minerals",
            "dinner": "Soup + salad – digestive rest"
        },
        "Day 3": {
            "breakfast": "Eggs / paneer toast – muscle repair",
            "lunch": "Rice + chicken / chole – protein boost",
            "dinner": "Steamed vegetables – gut health"
        },
        "Day 4": {
            "breakfast": "Upma / poha – slow energy release",
            "lunch": "Millet roti + sabzi – metabolism support",
            "dinner": "Curd + light meal – gut balance"
        },
        "Day 5": {
            "breakfast": "Sprouts – enzyme activation",
            "lunch": "Vegetable khichdi – easy digestion",
            "dinner": "Roti + dal – protein balance"
        },
        "Day 6": {
            "breakfast": "Banana + nuts – quick energy",
            "lunch": "Rice + fish / tofu – omega-3 support",
            "dinner": "Soup – inflammation control"
        },
        "Day 7": {
            "breakfast": "Choice meal (controlled) – mental satisfaction",
            "lunch": "Balanced plate – sustainability",
            "dinner": "Light food – body recovery"
        }
    }

    # ---------- WEEKLY EXERCISE PLAN ----------
    weekly_exercise = {
        "Day 1": "Brisk walking – 20 min (heart health)",
        "Day 2": "Strength training – 30 min (muscle building)",
        "Day 3": "Yoga & stretching – recovery",
        "Day 4": "Jogging + core – 30 min",
        "Day 5": "Lower body workout – strength",
        "Day 6": "Mobility & flexibility – joint health",
        "Day 7": "Complete rest – muscle recovery"
    }

    # ---------- STRESS RELIEF PLAN ----------
    stress_plan = {
        "Day 1": "Deep breathing – nervous system calm",
        "Day 2": "Listen to calming music",
        "Day 3": "Read books like Atomic Habits or Ikigai",
        "Day 4": "Talk with friends or family",
        "Day 5": "Evening walk without phone",
        "Day 6": "Digital detox for 2 hours",
        "Day 7": "Self-reflection & journaling"
    }

    # ---------- MENTAL WELL-BEING ----------
    mental_wellbeing = (
        "Mental well-being routines reduce anxiety, improve focus, and build emotional "
        "resilience. Practicing gratitude, mindful breathing, and maintaining social "
        "connections helps sustain long-term mental health."
    )
    # ---------- PERSONALIZED MENTAL WELL-BEING DETAILS ----------

    # Gratitude based on job / stress
    if profile.stress_level == 'high':
        gratitude_text = (
        "Since your stress level is high, practicing gratitude helps your mind shift away "
        "from constant pressure. Every night, write down three small things that went well "
        "during your workday, such as completing a task or taking a short break."
     )
    elif profile.stress_level == 'medium':
        gratitude_text = (
        "Practicing gratitude helps maintain emotional balance. Spend a few minutes daily "
        "acknowledging positive moments at work or in personal life."
        )
    else:
        gratitude_text = (
        "Your stress levels are currently low. Gratitude practice helps sustain positivity "
        "and emotional stability over time."
        )

    # Mindful breathing based on activity & job nature
    if profile.activity_level == 'low':
        breathing_text = (
            "Since you spend long hours sitting or doing desk-based work, mindful breathing "
            "helps reduce mental fatigue. Practice slow breathing for 5–10 minutes during work "
            "breaks to relax your nervous system."
        )

    else:
        breathing_text = (
        "Mindful breathing helps your body recover after physical or mentally demanding "
        "activities. Practicing it after exercise or before sleep improves relaxation."
     )

    # Social interaction (introvert-friendly)
    social_text = (
         "If you prefer limited social interaction or feel introverted, focus on quality over quantity. "
        "Connect with one trusted person through messages or short conversations. "
        "Gradually engaging in interest-based groups helps build comfort without pressure."
    )

    mental_habits_text = (
        "Maintain a consistent sleep schedule, limit screen usage before bedtime, and spend "
        "at least 15 minutes daily on calming activities such as reading, walking, or listening "
        "to music. These habits improve long-term mental resilience."
    )


    return {
        "bmi": bmi,
        "bmi_status": bmi_status,
        "bmi_advice": bmi_advice,
        "health_overview": health_overview,
        "calorie_explanation": calorie_explanation,
        "weekly_meals": weekly_meals,
        "weekly_exercise": weekly_exercise,
        "stress_plan": stress_plan,
        "mental_wellbeing": mental_wellbeing,
        "current_calories": current_calories,
        "target_calories": target_calories,
        "calorie_action": calorie_action,
        "calorie_advice": calorie_advice,
        "gratitude_text": gratitude_text,
        "breathing_text": breathing_text,
        "social_text": social_text,
        "mental_habits_text": mental_habits_text,
    }

def generate_food_recommendation(
    purpose, meal_time, food_type, diet_type,
    health_condition, calorie_target,
    cuisine, spice_level, preparation_time
):

    # ---------- REAL FOOD SELECTION ----------
    if cuisine == "south_indian" and diet_type == "veg":
        dish = "Vegetable Upma"
        ingredients = [
            "1 cup semolina (rava)",
            "1 cup mixed vegetables (carrot, beans, peas)",
            "1 tsp mustard seeds",
            "1 tsp oil",
            "Curry leaves",
            "Salt to taste"
        ]
        steps = [
            "Dry roast semolina for 3-4 minutes.",
            "Heat oil and add mustard seeds & curry leaves.",
            "Add vegetables and sauté for 5 minutes.",
            "Add 2 cups water and bring to boil.",
            "Slowly add semolina while stirring.",
            "Cook for 3-4 minutes until soft."
        ]

    elif cuisine == "south_indian" and diet_type == "nonveg":
        dish = "Egg Bhurji with Millet Roti"
        ingredients = [
            "2 eggs",
            "1 small onion (chopped)",
            "1 tomato (chopped)",
            "Millet flour roti",
            "Turmeric & spices"
        ]
        steps = [
            "Heat oil and sauté onions.",
            "Add tomatoes and cook until soft.",
            "Add beaten eggs and stir continuously.",
            "Cook until fluffy.",
            "Serve with warm millet roti."
        ]

    else:
        dish = f"{cuisine.replace('_',' ').title()} {diet_type} {food_type}"
        ingredients = ["Balanced ingredients based on selected preferences"]
        steps = ["Prepare using healthy cooking methods such as steaming or sautéing."]

    # ---------- FORMAT TEXT PROPERLY ----------
    ingredients_text = "\n- ".join(ingredients)
    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

    # ---------- BENEFITS ----------
    benefit_text = f"This dish supports {purpose.replace('_',' ')}."

    if purpose == "weight_loss":
        benefit_text += " It is fiber-rich and keeps you full longer."
    elif purpose == "muscle_gain":
        benefit_text += " It provides high-quality protein for muscle repair."

    if health_condition != "none":
        benefit_text += f" It is designed to help manage {health_condition}."

    # ---------- CALORIES ----------
    if calorie_target == "low":
        calories = "250-300 kcal"
    elif calorie_target == "moderate":
        calories = "350-450 kcal"
    else:
        calories = "500-650 kcal"

    # ---------- RETURN STRUCTURED OUTPUT ----------
    return f"""
🍽 Recommended Dish: {dish}

🕒 Best Time: {meal_time.replace('_',' ').title()}

🔥 Calories:
Approximately {calories} per serving.

🛒 Ingredients:
- {ingredients_text}

👨‍🍳 Preparation Steps:
{steps_text}

💪 Health Benefits:
{benefit_text}

😊 Mood & Brain Impact:
Rich in nutrients that improve serotonin levels and stabilize energy.

🌶 Spice Level:
{spice_level.title()}

🥗 Portion Suggestion:
1 medium bowl or 2 medium rotis equivalent.

💡 Pro Tip:
Avoid deep frying. Prefer steaming, grilling, or light sautéing.
"""
