import face_recognition
import base64
from PIL import Image
import io
import numpy as np

class ImageConverter:
    def image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def base64_to_image(self, base64_str):
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGB")  # Ensure image is in RGB format
        return np.array(image)


class FaceComparer:
    def __init__(self, converter=None):
        self.converter = converter if converter else ImageConverter()

    def compare_faces(self, image1_path, image2_path):
        image1_base64 = self.converter.image_to_base64(image1_path)
        image2_base64 = self.converter.image_to_base64(image2_path)
        
        img1 = self.converter.base64_to_image(image1_base64)
        img2 = self.converter.base64_to_image(image2_base64)

        face_encoding1 = face_recognition.face_encodings(img1)
        face_encoding2 = face_recognition.face_encodings(img2)

        if not face_encoding1 or not face_encoding2:
            return "No faces found in one or both images."

        match = face_recognition.compare_faces([face_encoding1[0]], face_encoding2[0])
        return "The faces match!" if match[0] else "The faces do not match."
    
    def compare_faces_from_base64(self, image1_base64, image2_base64):
        img1 = self.converter.base64_to_image(image1_base64)
        img2 = self.converter.base64_to_image(image2_base64)

        face_encoding1 = face_recognition.face_encodings(img1)
        face_encoding2 = face_recognition.face_encodings(img2)

        if not face_encoding1 or not face_encoding2:
            return "No faces found in one or both images."

        match = face_recognition.compare_faces([face_encoding1[0]], face_encoding2[0])
        return "The faces match!" if match[0] else "The faces do not match."


# Example usage
# converter = ImageConverter()
# face_comparer = FaceComparer(converter)

# image1_path = "./shazi-1.png"
# image2_path = "./shazi-2.png"

# result = face_comparer.compare_faces(image1_path, image2_path)
# print(result)
