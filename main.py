from flask import Flask, request, jsonify
import cv2
import dlib
import numpy as np
import base64
from scipy.spatial import distance as dist
from flask_cors import CORS
from classes.face import FaceComparer
from classes.ear import EARCalculator

app = Flask(__name__)
cors = CORS(app, resources={r"/ear": {"origins": "*"}})

ear_calculator = EARCalculator('./model.dat')

@app.route('/ear', methods=['POST'])
def get_ear():
    try:
        data = request.json
        image_data = data['image']
        avg_ear = ear_calculator.get_ear_from_image(image_data)
        return jsonify({'ear': avg_ear}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/compare', methods=['POST'])
def compare_faces():
    data = request.json
    image1_base64 = data['image1']
    image2_base64 = data['image2']
    face_comparer = FaceComparer()
    result = face_comparer.compare_faces_from_base64(image1_base64, image2_base64)
    return jsonify({'result': result}), 200    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
