import os
from datetime import datetime, timedelta
from food_daily.code.detect_image import food_detector
from scripts.query import query_pipeline
from generate_answer.generate import weekly_tip


def summarize_weekly_risk_from_meals(meals):
    """
    Summarize daily and weekly average glycemic load (GL) based on recorded meals.

    Updated version:
    1. Groups meals by date (within past 7 days).
    2. Calculates total GL per day.
    3. Computes weekly average GL = (sum of daily GL) / (number of days with data or 7).
    4. Generates a weekly risk score (0–100 scale).
    """

    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    meals_this_week = []

    # Step 1: Filter meals from the last 7 days
    print(meals)
    for meal in meals:
        try:
            meal_date = datetime.strptime(meal['date'], "%Y-%m-%d").date()
        except Exception:
            continue
        if week_ago <= meal_date <= today:
            meals_this_week.append(meal)

    # Step 2: Group GL values by date
    daily_gl = {}  # { date: total_gl_for_that_day }
    context = "Meals this week:\n"

    for meal in meals_this_week:
        date_str = meal['date']
        context += f"- {date_str} {meal['name']} ({meal['description']})\n"
        nutrition_info = meal.get("nutrition_info", [])

        for food in nutrition_info:
            gi = food.get("gi")
            portion = food.get("portion", 100)
            carbs = food.get("carbohydrate", 0)

            try:
                gi_val = float(gi)
                portion_val = float(portion)
                carbs_val = float(carbs)

                # total carbs (grams) in the portion
                total_carbs = portion_val * carbs_val / 100
                # GL = (GI / 100) × total_carbs
                gl = (gi_val / 100) * total_carbs

                daily_gl[date_str] = daily_gl.get(date_str, 0) + gl

                context += (
                    f"    • {food.get('name', '')}: "
                    f"GI {gi}, portion {portion}g, "
                    f"carb per 100g {carbs}g, "
                    f"GL = ({gi}/100)×({portion}×{carbs}/100) = {gl:.1f}\n"
                )

            except Exception:
                continue

    # Step 3: Compute weekly average GL
    if daily_gl:
        total_gl_week = sum(daily_gl.values())
        num_days = len(daily_gl)  # actual number of days with data
        average_gl = total_gl_week / (7 if len(daily_gl) >= 7 else num_days)
    else:
        total_gl_week = 0.0
        average_gl = 0.0
        num_days = 0

    # Step 4: Compute risk score (0–100 scale)
    score = min(int((average_gl / 150) * 100), 100)

    # Step 5: Add summary to context
    context += "\nDaily GL Summary:\n"
    for d, gl_val in sorted(daily_gl.items()):
        context += f"  {d}: Total GL = {gl_val:.2f}\n"

    context += f"\nWeekly Total GL: {total_gl_week:.2f}\n"
    context += f"Average GL (per day): {average_gl:.2f} (over {num_days} days)\n"
    context += f"Weekly risk score: {score}\n"

    # Step 6: Generate weekly tip using AI
    summary = weekly_tip(context)

    print("Weekly Summary Context:\n", context)

    return summary, score
