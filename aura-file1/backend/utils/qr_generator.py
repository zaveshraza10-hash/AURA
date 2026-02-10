import qrcode
import base64
from io import BytesIO
import json
from datetime import datetime, timedelta

def generate_qr(user_id: str):
    # Create QR data with expiry
    data = {
        "user_id": user_id,
        "expiry": (datetime.utcnow() + timedelta(minutes=5)).isoformat(),
        "type": "atm_login"
    }
    
    # Generate QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str