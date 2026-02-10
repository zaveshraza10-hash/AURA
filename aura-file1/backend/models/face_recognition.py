"""
Simple Face Authentication using OpenCV only (No Dlib needed)
For demo purposes only
"""
import cv2
import numpy as np
import pickle
import os
import base64
from datetime import datetime

class SimpleFaceAuth:
    def __init__(self):
        self.face_database = {}
        self.load_database()
    
    def load_database(self):
        """Load mock face database"""
        # For demo, create 2 test users
        self.face_database = {
            "user_001": {
                "name": "John Doe",
                "account": "1234567890",
                "balance": 50000,
                "face_encoded": "demo_face_1"  # Mock encoding
            },
            "user_002": {
                "name": "Jane Smith", 
                "account": "0987654321",
                "balance": 75000,
                "face_encoded": "demo_face_2"
            }
        }
    
    def detect_face(self, image_path):
        """Simple face detection using OpenCV"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return False
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Load pre-trained face detector
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            return len(faces) > 0
            
        except Exception as e:
            print(f"Face detection error: {e}")
            return True  # For demo, always return True
    
    def verify_face(self, image_path):
        """
        Mock face verification
        In real app, you'd compare face encodings
        """
        # Check if face is detected
        if not self.detect_face(image_path):
            return None
        
        # For demo, always return first user
        # In hackathon demo, you can say this is mock
        return "user_001"
    
    def register_face(self, image_path, user_id, user_data):
        """Mock face registration"""
        self.face_database[user_id] = user_data
        return True
    
    def get_user_info(self, user_id):
        """Get user information"""
        return self.face_database.get(user_id)

# Create instance
face_auth = SimpleFaceAuth()