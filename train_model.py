"""
Train a plant disease detection model using transfer learning
This script uses a pre-trained model (MobileNetV2) and fine-tunes it on plant disease dataset
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 25

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

def create_model(num_classes):
    """
    Create a model using transfer learning with MobileNetV2
    """
    # Load pre-trained MobileNetV2
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base model
    base_model.trainable = False
    
    # Create new model on top
    inputs = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    
    return model

def train_model(train_dir, val_dir=None):
    """
    Train the plant disease detection model
    
    Args:
        train_dir: Path to training data directory
        val_dir: Path to validation data directory (optional)
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        validation_split=0.2 if val_dir is None else 0.0
    )
    
    # Load training data
    if val_dir is None:
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )
        
        val_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )
    else:
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
        
        val_datagen = ImageDataGenerator(rescale=1./255)
        val_generator = val_datagen.flow_from_directory(
            val_dir,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
    
    # Create model
    num_classes = len(train_generator.class_indices)
    model = create_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Print model summary
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=2,
            min_lr=0.00001
        )
    ]
    
    # Train model
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=callbacks
    )
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model.save('models/plant_disease_model.h5')
    print("\nModel saved to models/plant_disease_model.h5")
    
    # Print final metrics
    print("\nTraining completed!")
    print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    return model, history

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Train plant disease detection model')
    parser.add_argument('--train-dir', type=str, required=True,
                        help='Path to training data directory')
    parser.add_argument('--val-dir', type=str, default=None,
                        help='Path to validation data directory (optional)')
    parser.add_argument('--epochs', type=int, default=10,
                        help='Number of training epochs')
    
    args = parser.parse_args()
    
    EPOCHS = args.epochs
    
    print("Starting model training...")
    print(f"Training directory: {args.train_dir}")
    if args.val_dir:
        print(f"Validation directory: {args.val_dir}")
    print(f"Epochs: {EPOCHS}")
    
    model, history = train_model(args.train_dir, args.val_dir)
