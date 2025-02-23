import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from datetime import datetime
import os

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.6)

# Function to extract bounding box as NumPy array
def get_face_encoding(detection):
    bbox = detection.location_data.relative_bounding_box
    return np.array([bbox.xmin, bbox.ymin, bbox.width, bbox.height], dtype=np.float32)

# Function to load and encode known faces
def load_face_encodings(folder_path="faces"):
    known_face_encodings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            name = os.path.splitext(filename)[0]
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get face encodings
            results = face_detection.process(img_rgb)
            if results.detections:
                encoding = get_face_encoding(results.detections[0])
                known_face_encodings[name] = encoding
    return known_face_encodings

# Load known face encodings
known_faces = load_face_encodings()

# Prepare CSV file for attendance
current_date = datetime.now().strftime("%Y-%m-%d")
csv_file = f"{current_date}.csv"
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["Name", "Time"]).to_csv(csv_file, index=False)

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)

    name = "Unknown"

    if results.detections:
        for detection in results.detections:
            encoding = get_face_encoding(detection)

            # Compare with known faces
            for known_name, known_encoding in known_faces.items():
                distance = np.linalg.norm(known_encoding - encoding)
                if distance < 0.1:  # Adjust threshold as needed
                    name = known_name
                    break

            # Draw bounding box
            h, w, _ = frame.shape
            bbox = detection.location_data.relative_bounding_box
            x, y, w, h = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Log attendance if recognized
    if name != "Unknown":
        df = pd.read_csv(csv_file)
        if name not in df["Name"].values:
            with open(csv_file, "a") as f:
                f.write(f"{name},{datetime.now().strftime('%H:%M:%S')}\n")

    # Display video feed
    cv2.imshow("Attendance System", frame)

    # Press 'q' or 'Esc' to exit
    key = cv2.waitKey(1)
    if key & 0xFF == ord("q") or key == 27:
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
