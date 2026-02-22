# AgroVisionNet Configuration

# Application Settings
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Upload Settings
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Model Settings
MODEL_PATH = 'models/plant_disease_model.h5'
IMG_SIZE = 224
NUM_CLASSES = 25

# Training Settings
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001

# Supported Plant Types
SUPPORTED_PLANTS = [
    'Apple',
    'Corn (Maize)',
    'Grape',
    'Potato',
    'Tomato'
]

# Note: Modify these settings as needed for your deployment
