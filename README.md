# Face Recognition Attendance System

This project implements a real-time face recognition system designed to track student attendance using a webcam. Known faces are pre-loaded, and attendance is logged in a CSV file with timestamps when a recognized student appears in the video frame.

## Prerequisites

Before running this script, ensure you have the following libraries installed:

cmake (https://cmake.org/)
face_recognition (https://github.com/ageitgey/face_recognition)
opencv-python (https://pypi.org/project/opencv-python/)   
You can install them using pip:

Bash
pip install cmake
pip install face_recognition
pip install opencv-python
Use code with caution.

## Usage

Create a faces folder: Inside this folder, place image files of the known individuals whose attendance you want to track. Name the files appropriately (e.g., sample1.png, sample2.jpg).
Run the script: Execute the Python script using your preferred terminal or command prompt.
## Explanation

The script follows these key steps:

Import Libraries: Necessary libraries for face recognition, image processing, and date/time manipulation are imported.
Initialize Video Capture: A webcam stream is accessed using OpenCV's VideoCapture class.
Load Reference Images: Images of known individuals are loaded using face_recognition.load_image_file and their corresponding encodings are generated using face_recognition.face_encodings.
Define Known Faces: A list known_face_encodings stores these encodings, and a matching list known_face_names stores their names.
Create Student Attendance List: A copy of known_face_names is created as students to track present students.
Main Loop: The loop continues until the user presses the 'q' key.
Capture Frame: A frame is read from the webcam.
Resize Frame: The frame is resized for faster processing using cv2.resize.
Convert Colorspace: The frame is converted from BGR to RGB for face recognition using cv2.cvtColor.
Detect Faces: Potential faces are identified in the frame using face_recognition.face_locations.
Encode Faces: Encodings are generated for each detected face using face_recognition.face_encodings.
Recognize Faces: Each detected face's encoding is compared to the known encodings using face_recognition.compare_faces.
Record Attendance: If a match is found, the student's name is retrieved, and if present in the students list (indicating they haven't been marked yet), their name and timestamp are recorded in a CSV file using csv.writer.
Display Results: The frame is displayed with labels indicating recognized individuals (or "Unknown" if not recognized).
Release Resources: The webcam capture is released, and all windows are closed.
Close CSV File: The CSV file containing attendance records is closed.
## CSV Output

The script creates a CSV file named with the current date (YYYY-MM-DD). Each row in the CSV file contains the following columns:

Name: The name of the recognized student.
Time: The timestamp when the student was recognized (HH:MM:SS).
## Customization

You can add more reference images to faces to include additional individuals.
Modify the students list to adjust the list of expected students.
Customize the CSV file format or location if needed.
## Disclaimer

This project may not be suitable for real-world applications due to factors like lighting variations, occlusions, and potential performance limitations.

## License

This project is open-source and available under the [MIT License](LICENSE).
