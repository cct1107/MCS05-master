from scripts.query import query_pipeline
from generate_answer.generate import process_meal

def process_nutrition_info(description, nutrition_info):

    meal = {
        "description": description,
        "nutrition_info": nutrition_info
    }
    new_nutrition_info = process_meal(meal)
    print("++++++++++++++++++++++++++++++++++++++++++")
    print("Processed Nutrition Info:", new_nutrition_info)
    return new_nutrition_info