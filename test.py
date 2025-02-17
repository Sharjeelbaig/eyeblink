import face_recognition
import base64
from PIL import Image
import io
import numpy as np
import cv2

# Function to convert an image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to convert base64 to an image
def base64_to_image(base64_str):
    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data))
    return np.array(image)

# Function to compare faces
def compare_faces(image1_path, image2_path):
    # Convert images to base64
    image1_base64 = image_to_base64(image1_path)
    image2_base64 = image_to_base64(image2_path)
    
    # Decode base64 back to image
    img1 = base64_to_image(image1_base64)
    img2 = base64_to_image(image2_base64)

    # Find face encodings for both images
    face_encoding1 = face_recognition.face_encodings(img1)
    face_encoding2 = face_recognition.face_encodings(img2)

    if not face_encoding1 or not face_encoding2:
        return "No faces found in one or both images."
    
    # Compare the two faces
    match = face_recognition.compare_faces([face_encoding1[0]], face_encoding2[0])

    if match[0]:
        return "The faces match!"
    else:
        return "The faces do not match."

# Example usage
image1_path = "./shazi-1.png"  # Path to your first image
image2_path = "./shazi-2.png"  # Path to your second image

result = compare_faces(image1_path, image2_path)
print(result)
