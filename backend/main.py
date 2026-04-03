import datetime
import sys, os, uuid
from typing import Optional
from fastapi import Body, FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool
import base64
from fastapi import Request


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.query import query_pipeline
from food_daily.code.detect_image import food_detector_bytes
from food_daily.code.weekly import summarize_weekly_risk_from_meals
from food_daily.code.logMeal import process_nutrition_info
from generate_answer.generate import individual_food_analysis


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
PROCESS_FLAG = os.path.join(UPLOAD_DIR, "aiprocessing.lock")  
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.post("/chat")
def chat_endpoint(data: QueryRequest):
    reply = query_pipeline(data.query)
    return {
        "reply": reply,
        "foods": [],
        "image_url": None,
        "used_context": data.query,
        "original_query": data.query
    }

@app.post("/chat/submit")
async def chat_submit(
    query: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    foods = []
    image_url = None
    final_query = query
    print("Received query:", query)

    if file:
        raw = await file.read()
        foods = await run_in_threadpool(food_detector_bytes, raw)
        if foods:
            # Build context with GI / GL / Carbohydrate
            detail_line = ", ".join([
                f"{f['name']} (GI {f['gi']}, GL {f['gl']}, Carb {f['carbohydrate']}g)"
                for f in foods
            ])
        else:
            detail_line = "No foods detected"
        foods_context = f"Detected foods: {detail_line}"
        final_query = f"{query}\n\n{foods_context}"

    if foods:
        is_detected = True
    else:
        is_detected = False

    print("[chat_submit] is_detected:", is_detected)
    print("[chat_submit] Final query:\n", final_query)

 
    reply = await run_in_threadpool(query_pipeline, final_query, is_detected)


    return {
        "reply": reply,
        "foods": foods,
        "image_url": None,
        "used_context": final_query,
        "original_query": query,
        "is_detected": is_detected
    }


@app.post("/meals/add")
async def add_meal(
    name: str = Body(...),
    description: str = Body(...),
    date: str = Body(...),
    time: str = Body(...),
    file: str = Body(None),
    recent_meals: list = Body([])
):
        # if have processing flag, return conflict response 409
    if os.path.exists(PROCESS_FLAG):
        return JSONResponse({"success": False, "error": "processing_in_progress"}, status_code=409)

    # build processing flag
    try:
        with open(PROCESS_FLAG, "w", encoding="utf-8") as f:
            f.write(str(datetime.datetime.utcnow().isoformat()))
    except Exception:
        pass

    try:
        recent_meals_remove_image = []
        for meal in recent_meals:
            meal_copy = dict(meal)
            meal_copy.pop("image_url", None)
            meal_copy.pop("image", None)
            recent_meals_remove_image.append(meal_copy)

        image_url = None
        nutrition_info = []
        if file:
            raw = base64.b64decode(file.split(",")[-1])
            foods = await run_in_threadpool(food_detector_bytes, raw)
            for food in foods:
                nutrition_info.append({
                    "name": food.get("name"),
                    "gi": food.get("gi"),
                    "gl": food.get("gl"),
                    "carbohydrate": food.get("carbohydrate"),
                    "portion": 50
                })
            
        upload_nutrition_info = await run_in_threadpool(process_nutrition_info, description, nutrition_info)
        cleaned_recent_meals = []
        for meal in recent_meals:
            meal_copy = dict(meal)
            meal_copy.pop("image_url", None)
            meal_copy.pop("image", None)
            cleaned_recent_meals.append(meal_copy)
        meals_list = cleaned_recent_meals
        meal = {
            "name": name,
            "description": description,
            "date": date,
            "time": time,
            "nutrition_info": upload_nutrition_info
        }
        analysis = await run_in_threadpool(individual_food_analysis, meal, description)

        recent_meals_remove_image.append(meal)

        print(meals_list)
        summary, score = summarize_weekly_risk_from_meals(recent_meals_remove_image)
        meal = {
            "name": name,
            "description": description,
            "date": date,
            "time": time,
            "image_url": image_url,
            "nutrition_info": upload_nutrition_info,
            "analysis": analysis
        }

        return JSONResponse({
            "success": True,
            "meal": meal,
            "summary": summary,
            "score": score
        })
    finally:
            # confirm to remove processing flag
            try:
                if os.path.exists(PROCESS_FLAG):
                    os.remove(PROCESS_FLAG)
            except Exception:
                pass

@app.post("/meals/weekly-summary")
async def weekly_summary(request: Request):
    if os.path.exists(PROCESS_FLAG):
        return JSONResponse({"success": False, "error": "processing_in_progress"}, status_code=409)

    # create flag with timestamp
    try:
        with open(PROCESS_FLAG, "w", encoding="utf-8") as f:
            f.write(str(datetime.datetime.utcnow().isoformat()))
    except Exception:
        pass

    try:
        data = await request.json()
        meals = data.get("meals", [])
        cleaned_meals = []
        for meal in meals:
            meal_copy = dict(meal)
            meal_copy.pop("image", None)
            meal_copy.pop("image_url", None)
            cleaned_meals.append(meal_copy)
        summary, score = summarize_weekly_risk_from_meals(cleaned_meals)
        return {"summary": summary, "score": score}
    finally:
        # ensure flag removed before returning
        try:
            if os.path.exists(PROCESS_FLAG):
                os.remove(PROCESS_FLAG)
        except Exception:
            pass

# endpoint for front-end polling of processing status
@app.get("/processing-status")
async def processing_status():
    status = os.path.exists(PROCESS_FLAG)
    return {"aiprocessing": status}

if __name__ == "__main__":

    query = "how to lower my risk of prediabetes？"

    answer = query_pipeline(query)

    print("Answer:")
    print(answer)