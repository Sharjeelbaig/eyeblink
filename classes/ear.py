from scipy.spatial import distance as dist
import numpy as np
import cv2
import dlib
import base64

class EARCalculator:
    def __init__(self, model_path: str):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(model_path)

    @staticmethod
    def calculate_ear(eye: np.ndarray) -> float:
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C)

    def get_ear_from_image(self, image_data: str) -> float:
        np_img = np.frombuffer(base64.b64decode(image_data), np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        
        if not faces:
            raise ValueError('No face detected')
        
        face = faces[0]
        landmarks = self.predictor(gray, face)
        landmarks_points = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)])

        left_ear = self.calculate_ear(landmarks_points[42:48])
        right_ear = self.calculate_ear(landmarks_points[36:42])
        
        return (left_ear + right_ear) / 2.0
