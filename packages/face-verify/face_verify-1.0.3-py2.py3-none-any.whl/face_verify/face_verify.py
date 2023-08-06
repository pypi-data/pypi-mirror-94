# -*- coding: utf-8 -*-
import PIL.Image
import dlib
import numpy as np
import io
import base64
import json

try:
    import face_recognition_models
except Exception:
    print("Please install `face_recognition_models` with this command before using `face_recognition`:\n")
    print("pip install git+https://github.com/ageitgey/face_recognition_models")
    quit()

face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))
    return np.linalg.norm(face_encodings - face_to_compare, axis=1)

def _raw_face_locations(img):
    return face_detector(img)

def _raw_face_landmarks(face_image):
    face_locations = _raw_face_locations(face_image)
    pose_predictor = pose_predictor_68_point
    return [pose_predictor(face_image, face_location) for face_location in face_locations]

def face_encodings(face_image):
    raw_landmarks = _raw_face_landmarks(face_image)
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, 1)) for raw_landmark_set in raw_landmarks]

def verify(face, faces, tolerance = 0.6):
    face = face_encodings(base64ToNumpyArray(face))[0]
    for face_encoding in faces:
        json_image = json.loads(face_encoding)
        face_as_np =  np.array(json_image)
        distance = face_distance([face_as_np], face)
        if distance < tolerance:
            return True
    return False

def register(face):
    face_as_np = base64ToNumpyArray(face)
    face_encoding = face_encodings(face_as_np)
    if len(face_encoding):
        return str(list(face_encoding[0]))
    else:
        raise NameError("Face not detected")

def base64ToNumpyArray(base64_string):
    base64_string = base64.b64decode(base64_string.replace("data:image/png;base64,", ""))
    buf = io.BytesIO(base64_string)
    img = PIL.Image.open(buf).convert('RGB')
    return np.array(img, dtype=np.uint8)