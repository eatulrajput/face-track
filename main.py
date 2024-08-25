# pip install cmake
# pip install face_recognition
# pip install opencv-python

import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

# Load known faces
sample1_image = face_recognition.load_image_file("faces/sample1.png")
sample1_encoding = face_recognition.face_encodings(sample1_image)[0]

sample2_image = face_recognition.load_image_file("faces/sample2.png")
sample2_encoding = face_recognition.face_encodings(sample2_image)[0]

known_face_encodings = [sample1_encoding, sample2_encoding]
known_face_names = ["Sample1", "Sample2"]

# List of expected students
students = known_face_names.copy()

face_locations = []
face_encodings = []

# Get the correct date and time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Recognize faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        name = "Unknown"
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            if name in students:
                students.remove(name)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                lnwriter.writerow([name, current_time])

        # Add the text if the person is present
        if name != "Unknown":
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 255, 255)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + " Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)

    # Display the resulting image
    cv2.imshow("Attendance", frame)

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the capture
video_capture.release()
cv2.destroyAllWindows()
f.close()
