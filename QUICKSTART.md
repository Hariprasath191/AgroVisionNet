# Quick Start Guide

## Getting Started with AgroVisionNet

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Hariprasath191/AgroVisionNet.git
cd AgroVisionNet

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

#### Option A: Web Application (Recommended)

```bash
python app.py
```

Then open your browser and go to: `http://localhost:5000`

#### Option B: Command Line

```bash
python predict.py path/to/your/plant/image.jpg
```

### 3. Training Your Own Model

To train a custom model with your own dataset:

```bash
python train_model.py --train-dir /path/to/dataset --epochs 10
```

**Dataset Structure:**
```
dataset/
├── Apple___Apple_scab/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Tomato___healthy/
│   └── ...
└── ...
```

### 4. Using the Web Interface

1. **Upload Image**: Click on the upload box or drag and drop a plant image
2. **Analyze**: Click the "Analyze Plant" button
3. **View Results**: See the plant type, disease status, and confidence level

### 5. API Usage

You can also use the application as an API:

```python
import requests

url = 'http://localhost:5000/predict'
files = {'file': open('plant_image.jpg', 'rb')}
response = requests.post(url, files=files)
result = response.json()

print(f"Plant: {result['plant']}")
print(f"Disease: {result['disease']}")
print(f"Confidence: {result['confidence']}%")
```

### 6. Supported Image Formats

- JPG/JPEG
- PNG

### 7. Model Information

The application uses **MobileNetV2** with transfer learning to classify plant diseases. It can detect:

- 25 different disease classes
- 5 plant types (Apple, Corn, Grape, Potato, Tomato)
- Both diseased and healthy plants

### 8. Troubleshooting

**Model not found error:**
- If you see "Model not found", you need to train a model first
- Download a pre-trained model or train your own using `train_model.py`

**Image upload fails:**
- Check that the image is in JPG or PNG format
- Ensure the image size is under 16MB

**Port already in use:**
- Change the port in `app.py` by modifying: `app.run(debug=True, host='0.0.0.0', port=5000)`

### 9. Performance Tips

- Use images with clear plant leaves for best results
- Ensure good lighting in photos
- Avoid blurry or low-resolution images
- Center the plant leaf in the frame

### 10. Next Steps

- Collect more training data to improve accuracy
- Fine-tune the model for specific crops
- Add treatment recommendations
- Integrate with agricultural databases

## Need Help?

Check the [main README](README.md) for detailed documentation or open an issue on GitHub.
