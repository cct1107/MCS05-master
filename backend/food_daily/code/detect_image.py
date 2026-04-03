import os
from functools import lru_cache
from typing import List, Dict
from ultralytics import YOLO
from .food_nutrition import search_gi_value
from PIL import Image
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../.."))
MODEL_PATH = os.path.join(ROOT_DIR, "backend", "food_daily", "weights.pt")

@lru_cache(maxsize=1)
def get_model_path() -> str:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return MODEL_PATH

def _post_process(class_names: List[str]) -> List[Dict[str, str]]:
    uniq, seen = [], set()
    for n in class_names:
        if n not in seen:
            seen.add(n)
            uniq.append(n)

    if "Curry-Puff" in uniq and "Karipap" in uniq:
        uniq = [n for n in uniq if n != "Karipap"]
    out = []
    for name in uniq:
        gi_info = search_gi_value(name)
        gi_value = gi_info.get("gi_value") if gi_info else "N/A"
        gl_value = gi_info.get("gl_value") if gi_info else "N/A"
        carb_value = gi_info.get("carbohydrate") if gi_info else "N/A"
        out.append({
            "name": name,
            "gi": gi_value,
            "gl": gl_value,
            "carbohydrate": carb_value
        })
    return out

def food_detector(image_path: str):
    model = YOLO(get_model_path())
    results = model.predict(source=image_path, conf=0.25, save=False, verbose=False)
    detected = []
    for r in results:
        names = r.names
        for box in r.boxes:
            detected.append(names[int(box.cls[0])])
    return _post_process(detected)

def food_detector_bytes(raw: bytes) -> List[Dict[str, str]]:
    
    img = Image.open(BytesIO(raw)).convert("RGB")
    model =  YOLO(get_model_path())
    results = model.predict(source=img, conf=0.25, save=False, verbose=False)
    detected = []
    for r in results:
        names = r.names
        for box in r.boxes:
            detected.append(names[int(box.cls[0])])
    return _post_process(detected)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../.."))

    image_path = os.path.join(ROOT_DIR, "backend/food_daily/datasets/test/download (1).jpeg")
    model_path = os.path.join(ROOT_DIR, "backend", "food_daily", "weights.pt")  
    detection_names = food_detector(image_path)

    for name in detection_names:
        nutrition_info = search_gi_value(name)
        print(f"Nutrition info for {name}: {nutrition_info}")

    print(search_gi_value("fried chicken"))