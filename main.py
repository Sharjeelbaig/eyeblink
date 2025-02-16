import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist

# Eye Aspect Ratio (EAR) calculation
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Constants for drowsiness detection
EAR_THRESHOLD = 0.25  # EAR below this indicates eyes closed
CONSEC_FRAMES = 20    # Number of consecutive frames for drowsiness

frame_counter = 0

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./model.dat')

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        landmarks_points = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)])

        # Eye landmarks: left eye (42-47), right eye (36-41)
        leftEye = landmarks_points[42:48]
        rightEye = landmarks_points[36:42]

        # Compute EAR
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        avgEAR = (leftEAR + rightEAR) / 2.0

        # Draw eye landmarks
        # cv2.polylines(frame, [leftEye], True, (0, 255, 0), 1)
        # cv2.polylines(frame, [rightEye], True, (0, 255, 0), 1)

        # Drowsiness detection
        if avgEAR < EAR_THRESHOLD:
            frame_counter += 1
            if frame_counter >= CONSEC_FRAMES:
                cv2.putText(frame, "DROWSINESS ALERT!", (150, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            frame_counter = 0

        # Display EAR on frame
        cv2.putText(frame, f'EAR: {avgEAR:.2f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
