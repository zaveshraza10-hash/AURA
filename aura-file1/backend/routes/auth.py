from fastapi import APIRouter, UploadFile, File
import shutil
from models.face_recognition import FaceAuth
from utils.qr_generator import generate_qr

router = APIRouter()
face_auth = FaceAuth()

@router.post("/face-login")
async def face_login(file: UploadFile = File(...)):
    # Save uploaded image
    with open("temp_face.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    user_id = face_auth.verify_face("temp_face.jpg")
    if user_id:
        return {"status": "success", "user_id": user_id, "message": "Face recognized"}
    return {"status": "fail", "message": "Face not recognized"}

@router.get("/generate-qr/{user_id}")
async def get_qr(user_id: str):
    qr_data = generate_qr(user_id)
    return {"qr_code": qr_data}