import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../.."))

data_yaml = os.path.join(
    ROOT_DIR,
    "backend", "food_daily", "datasets", "Malaysian-Food-Recognition--1", "data.yaml"
)


os.system(
    f"yolo task=detect mode=train "
    f"model=yolo11s.pt "  
    f"data={data_yaml} "
    f"epochs=50 "
    f"imgsz=640 "
    f"batch=2 "
    f"device=cpu "
    f"workers=0"
)

print("train complete and model is stored in runs/detect/train/weights/best.pt")
