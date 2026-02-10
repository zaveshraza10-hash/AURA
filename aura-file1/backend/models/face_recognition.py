import cv2
import face_recognition
import numpy as np
import pickle
import os

class FaceAuth:
    def __init__(self):
        self.known_encodings = []
        self.known_users = []
        self.load_existing_faces()
    
    def load_existing_faces(self):
        if os.path.exists("face_data.pkl"):
            with open("face_data.pkl", "rb") as f:
                data = pickle.load(f)
                self.known_encodings = data["encodings"]
                self.known_users = data["users"]
    
    def register_face(self, image_path, user_id):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            self.known_encodings.append(encodings[0])
            self.known_users.append(user_id)
            self.save_faces()
            return True
        return False
    
    def verify_face(self, image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            return None
        
        matches = face_recognition.compare_faces(self.known_encodings, encodings[0])
        if True in matches:
            idx = matches.index(True)
            return self.known_users[idx]
        return None
    
    def save_faces(self):
        with open("face_data.pkl", "wb") as f:
            pickle.dump({"encodings": self.known_encodings, "users": self.known_users}, f)