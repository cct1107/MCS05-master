import pandas as pd
from pathlib import Path

def get_food_information(food_name: str) -> pd.DataFrame:
    """
    Retrieve food information from a CSV file based on the food name.
    Always reloads the CSV on each call.
    """
    
    csv_path = Path(__file__).resolve().parent.parent / "documents" / "Food GI_GL for food trained in model.csv"

    
    df = pd.read_csv(csv_path)

   
    df["FoodName"] = df["FoodName"].str.lower().str.replace("-", " ")

    
    food_name = food_name.lower().replace("-", " ")

    
    food_info = df[df["FoodName"] == food_name]

    food_info = food_info.head(1).reset_index(drop=True)
    return food_info

