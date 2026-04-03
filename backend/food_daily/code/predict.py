import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../.."))

model_path = os.path.join(ROOT_DIR, "runs", "detect", "train7", "weights", "best.pt")

source_path = os.path.join(ROOT_DIR, "backend", "food_daily", "datasets", "Malaysian-Food-Recognition--1", "test", "images")


os.system(
    f"yolo task=detect mode=predict model={model_path} conf=0.25 source={source_path} save=True"
)

print("The inference is completed and the results are stored in runs/detect/predict/")
