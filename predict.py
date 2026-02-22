"""
Utility script to make predictions on individual images
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import sys
import os

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

def load_model(model_path='models/plant_disease_model.h5'):
    """Load the trained model"""
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        print("Please train the model first using train_model.py")
        return None
    
    try:
        model = keras.models.load_model(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def preprocess_image(image_path, img_size=224):
    """Preprocess image for prediction"""
    try:
        img = Image.open(image_path)
        img = img.resize((img_size, img_size))
        img_array = np.array(img)
        
        # Ensure RGB format
        if len(img_array.shape) == 2:  # Grayscale
            img_array = np.stack([img_array] * 3, axis=-1)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = img_array[:, :, :3]
        
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict(model, image_path):
    """Make prediction on an image"""
    # Preprocess image
    img_array = preprocess_image(image_path)
    if img_array is None:
        return None
    
    # Make prediction
    predictions = model.predict(img_array, verbose=0)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class_idx])
    
    # Get disease information
    disease_name = DISEASE_CLASSES[predicted_class_idx]
    plant_name = disease_name.split('___')[0].replace('_', ' ')
    disease_status = disease_name.split('___')[1].replace('_', ' ')
    
    return {
        'plant': plant_name,
        'disease': disease_status,
        'confidence': round(confidence * 100, 2),
        'class_index': predicted_class_idx
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path> [model_path]")
        print("Example: python predict.py plant_image.jpg")
        print("         python predict.py plant_image.jpg models/plant_disease_model.h5")
        sys.exit(1)
    
    image_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else 'models/plant_disease_model.h5'
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)
    
    # Load model
    print("Loading model...")
    model = load_model(model_path)
    if model is None:
        sys.exit(1)
    
    # Make prediction
    print(f"\nAnalyzing image: {image_path}")
    result = predict(model, image_path)
    
    if result:
        print("\n" + "="*50)
        print("PREDICTION RESULTS")
        print("="*50)
        print(f"Plant Type:      {result['plant']}")
        print(f"Disease Status:  {result['disease']}")
        print(f"Confidence:      {result['confidence']}%")
        print("="*50)
    else:
        print("Prediction failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
