"""
Helper script with information about obtaining plant disease datasets
"""

import os

def print_dataset_info():
    """Print information about obtaining plant disease datasets"""
    print("=" * 70)
    print("Plant Disease Dataset Information")
    print("=" * 70)
    print()
    print("To train the AgroVisionNet model, you'll need a plant disease dataset.")
    print()
    print("RECOMMENDED DATASET:")
    print("-" * 70)
    print("PlantVillage Dataset")
    print("  - Contains 54,000+ images")
    print("  - 38 different plant disease classes")
    print("  - Available on Kaggle and other platforms")
    print()
    print("KAGGLE DATASET:")
    print("-" * 70)
    print("Dataset: PlantVillage Dataset")
    print("URL: https://www.kaggle.com/datasets/emmarex/plantdisease")
    print()
    print("ALTERNATIVE SOURCES:")
    print("-" * 70)
    print("1. GitHub: https://github.com/spMohanty/PlantVillage-Dataset")
    print("2. Official: https://plantvillage.psu.edu/")
    print()
    print("DATASET STRUCTURE:")
    print("-" * 70)
    print("The dataset should be organized as follows:")
    print()
    print("  dataset/")
    print("  ├── Apple___Apple_scab/")
    print("  │   ├── image1.jpg")
    print("  │   ├── image2.jpg")
    print("  │   └── ...")
    print("  ├── Apple___Black_rot/")
    print("  │   └── ...")
    print("  ├── Tomato___healthy/")
    print("  │   └── ...")
    print("  └── ...")
    print()
    print("DOWNLOADING DATASET:")
    print("-" * 70)
    print("Option 1: Kaggle CLI (if you have Kaggle API configured)")
    print("  kaggle datasets download -d emmarex/plantdisease")
    print("  unzip plantdisease.zip -d dataset/")
    print()
    print("Option 2: Manual Download")
    print("  1. Visit the Kaggle dataset page")
    print("  2. Download the dataset")
    print("  3. Extract to the 'dataset' directory")
    print()
    print("TRAINING THE MODEL:")
    print("-" * 70)
    print("Once you have the dataset, train the model:")
    print("  python train_model.py --train-dir dataset/ --epochs 10")
    print()
    print("=" * 70)
    print()

def create_dataset_directory():
    """Create dataset directory structure"""
    os.makedirs('dataset', exist_ok=True)
    print("✓ Created 'dataset' directory")
    print("  Place your plant disease images in this directory")
    print()

if __name__ == '__main__':
    print_dataset_info()
    
    response = input("Would you like to create the dataset directory? (y/n): ")
    if response.lower() == 'y':
        create_dataset_directory()
    
    print("\nFor more information, visit:")
    print("https://github.com/Hariprasath191/AgroVisionNet")
