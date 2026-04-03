import cv2
import os
from ultralytics import YOLO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../.."))

# model_path = os.path.join(ROOT_DIR, "runs/detect/train7/weights/best.pt")
model_path = os.path.join(ROOT_DIR, "backend", "food_daily", "weights.pt")

model = YOLO(model_path)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame, conf=0.25, save=False, verbose=False)


    for result in results:
        boxes = result.boxes
        names = result.names
        for box in boxes:
            cls_id = int(box.cls[0])
            cls_name = names[cls_id]
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            print(f"Detected: {cls_name}  Confidence={conf:.2f}  Box={xyxy}")

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            label = f"{cls_name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            

    cv2.imshow("Webcam Feed", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

