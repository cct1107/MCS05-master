import os
import pandas as pd
import csv
import requests
from typing import List, Optional, Dict
from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer("all-MiniLM-L6-v2")

API_URL = "https://world.openfoodfacts.org/cgi/search.pl"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
# GI_TABLE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../documents/GI_Table.csv"))
GI_TABLE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../documents/Food GI_GL for food trained in model.csv"))

gi_entries: List[Dict[str, str]] = []
gi_embeddings = None
all_names: List[str] = []

def get_food_nutrition(food_name: str, country: str = None) -> dict:
    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }
    if country:
        params["countries"] = country

    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("products"):
            product = data["products"][0]
            nutriments = product.get("nutriments", {})
            return {
                "product_name": product.get("product_name", "N/A"),
                "countries": product.get("countries_tags", []),
                "energy_kcal_100g": nutriments.get("energy-kcal_100g", "N/A"),
                "proteins_100g": nutriments.get("proteins_100g", "N/A"),
                "fat_100g": nutriments.get("fat_100g", "N/A"),
                "sugars_100g": nutriments.get("sugars_100g", "N/A"),
                "nutriscore": product.get("nutriscore_grade", "N/A")
            }
        
    return None

def get_nutrition_info(food_name: str) -> str:
    
    result = get_food_nutrition(food_name, country="Malaysia")
    if result:
        result["source"] = "Malaysia"
        return result
    
    result = get_food_nutrition(food_name)

    if result:
        result["source"] = "Global"
        return result
    
    return {"error": "Food item not found in the database."}


def extract_food_gi(file_path: str) -> list[str]:
    df = pd.read_csv(file_path)
    
    docs = []
    for _, row in df.iterrows():
        text = f"""
        Food: {row['Food Name']}
        GI: {row['GI']}
        Manufacturer: {row['Food Manufacturer'] if pd.notna(row['Food Manufacturer']) else 'Not specified'}
        Category: {row['Product Category']}
        Country: {row['Country']}
        Carbohydrate Portion: {row['Carbohydrate portion (g) / Average (g)']}
        GL: {row['GL']}
        Reference: {row['Reference']}
        Subject Type: {row['Subject Type']}
        """
        docs.append(text.strip())
    return docs

def load_gi_table_once(filepath: str = GI_TABLE_PATH):

    global gi_entries, all_names, gi_embeddings
    if gi_entries:
        return

    with open(GI_TABLE_PATH, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            entry = {
                "food_name": row["FoodName"].strip(),
                "gi_value": row["GI"].strip(),
                "gl_value": row["GL"].strip(),
                "carbohydrate": row["Carbohydrate portion(g)"].strip(),
            }
            gi_entries.append(entry)

    all_names = [entry["food_name"] for entry in gi_entries]
    gi_embeddings = embedder.encode(all_names, convert_to_tensor=True)



def search_gi_value(food_name: str) -> Optional[Dict[str, str]]:
    global gi_entries, gi_embeddings, all_names
    load_gi_table_once()  

    if not all_names or gi_embeddings is None:
        print("GI table is empty or not loaded properly.")
        return None

    query_embedding = embedder.encode(food_name, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, gi_embeddings)[0]

    best_idx = int(similarities.argmax())
    best_score = similarities[best_idx].item()

    result = gi_entries[best_idx].copy()
    return result