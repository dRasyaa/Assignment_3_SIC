from flask import Flask, request, jsonify
from deepface import DeepFace
import base64
import numpy as np
import cv2
import os
import requests

app = Flask(__name__)

def send_to_ubidots(is_keluarga):
    token = "BBUS-dUnnmdDGegd40VNGBKuCOnpvAbO9eJ"
    device = "neocane-dashboard"
    variable = "face_recognition"

    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{device}/"

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }

    payload = {
        variable: 1 if is_keluarga else 0
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        print(f"[Ubidots] Status keluarga: {payload['keluarga_terdeteksi']}, code: {res.status_code}")
    except Exception as e:
        print(f"[Ubidots] Error: {e}")

@app.route("/face-recognition", methods=["POST"])
def face_recognition_api():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        img_data = base64.b64decode(data["image"])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Failed to decode image"}), 400

        # Simpan temp image
        temp_path = "temp.jpg"
        cv2.imwrite(temp_path, img)

        # 💡 AUTO DETECT FOLDER DATABASE
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Data_Photo")

        # Debug print
        print("[DEBUG] db_path:", db_path)
        print("[DEBUG] Exists:", os.path.exists(db_path))

        if not os.path.exists(db_path):
            return jsonify({"error": "Database folder not found"}), 500

        result = DeepFace.find(img_path=temp_path, db_path=db_path, enforce_detection=False)

        if result and len(result[0]) > 0:
            best_match = result[0].iloc[0]
            identity_path = best_match['identity']
            nama = os.path.splitext(os.path.basename(identity_path))[0]
            send_to_ubidots(True)
            return jsonify({"status": "keluarga"})
        else:
            send_to_ubidots(False)
            return jsonify({"status": "unknown"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5510)
