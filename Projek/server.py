from flask import Flask, request, jsonify
import base64
import io
from PIL import Image
import numpy as np
import tensorflow as tf

# Inisialisasi Flask
app = Flask(__name__)

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path=r"C:\Denivo\Denivo Kren & misterius\MAN IC\SIC\Assignment_3_SIC\Projek\model_jalan.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Ukuran input model
target_size = input_details[0]['shape'][1:3]  # e.g. (128, 128)

def preprocess_image(img_base64):
    img_data = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_data)).convert('RGB')
    img = img.resize(target_size)
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        img_base64 = data['image']
        image = preprocess_image(img_base64)

        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        result = float(output_data[0][0])  # sigmoid output

        if result > 0.5:
            status = "jalan rusak"
        else:
            status = "aman"

        return jsonify({"status": status})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)