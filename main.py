from flask import Flask, request, jsonify
import cv2
import dlib
import numpy as np
import base64
from scipy.spatial import distance as dist
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/ear": {"origins": "*"}})

# Load dlib models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./model.dat')

class EARCalculator:
    @staticmethod
    def calculate(eye: np.ndarray) -> float:
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C)

@app.route('/ear', methods=['POST'])
def get_ear():
    data = request.json
    image_data = base64.b64decode(data['image'])
    np_img = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    if not faces:
        return jsonify({'error': 'No face detected'}), 400
    
    for face in faces:
        landmarks = predictor(gray, face)
        landmarks_points = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)])
        
        left_eye = landmarks_points[42:48]
        right_eye = landmarks_points[36:42]
        
        left_ear = EARCalculator.calculate(left_eye)
        right_ear = EARCalculator.calculate(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0
        
        return jsonify({'ear': avg_ear}), 200

    return jsonify({'error': 'No face landmarks detected'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
