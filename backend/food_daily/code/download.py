import os
from roboflow import Roboflow
import yaml
from pathlib import Path

rf = Roboflow(api_key="ufd6R4yTmDgDwph53QcH")
project = rf.workspace("fyp-uip0p").project("malaysian-food-recognition-xxeio")
dataset = project.version(1).download("yolov11")


dataset_path = Path(dataset.location)
yaml_file = dataset_path / "data.yaml"

with open(yaml_file, "r") as f:
    data = yaml.safe_load(f)

data["train"] = str(dataset_path / "train/images")
data["val"]   = str(dataset_path / "valid/images")
data["test"]  = str(dataset_path / "test/images")

with open(yaml_file, "w") as f:
    yaml.dump(data, f)

print("download complete and data.yaml updated!")
