from flask import Flask, request, jsonify
from deepface import DeepFace
import base64
import numpy as np
import cv2
import os

app = Flask(__name__)

@app.route("/face-recognition", methods=["POST"])
def face_recognition_api():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Decode base64
        img_data = base64.b64decode(data["image"])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Simpan sementara untuk compare
        cv2.imwrite("temp.jpg", img)

        # Cek match terhadap folder faces/
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Data_Photo")

        result = DeepFace.find(img_path="temp.jpg", db_path=db_path, enforce_detection=False)

        if result and len(result[0]) > 0:
            best_match = result[0].iloc[0]
            nama = best_match['identity'].split("\\")[-1].split(".")[0]
            return jsonify({"status": "keluarga", "nama": nama})
        else:
            return jsonify({"status": "unknown"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5510)
