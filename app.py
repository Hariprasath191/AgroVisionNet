from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Plant disease classes
DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Model loading placeholder
model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model():
    """Load the trained model"""
    global model
    try:
        model_path = 'models/plant_disease_model.h5'
        if os.path.exists(model_path):
            model = keras.models.load_model(model_path)
            print("Model loaded successfully!")
        else:
            print("Model file not found. Please train the model first.")
    except Exception as e:
        print(f"Error loading model: {e}")

def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_disease(image_path):
    """Predict plant disease from image"""
    if model is None:
        return {
            'disease': 'Model not loaded',
            'confidence': 0.0,
            'message': 'Please train and load the model first'
        }
    
    try:
        img_array = preprocess_image(image_path)
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        disease_name = DISEASE_CLASSES[predicted_class_idx]
        plant_name = disease_name.split('___')[0].replace('_', ' ')
        disease_status = disease_name.split('___')[1].replace('_', ' ')
        
        return {
            'plant': plant_name,
            'disease': disease_status,
            'confidence': round(confidence * 100, 2),
            'message': 'Prediction successful'
        }
    except Exception as e:
        return {
            'disease': 'Error',
            'confidence': 0.0,
            'message': f'Error during prediction: {str(e)}'
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        result = predict_disease(filepath)
        result['image_url'] = f'/static/uploads/{filename}'
        
        return jsonify(result)
    
    return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG'}), 400

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    # Load model on startup
    load_model()
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
