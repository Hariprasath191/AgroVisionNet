# AgroVisionNet 🌿

An AI-powered web application for detecting plant diseases using deep learning. This application uses transfer learning with MobileNetV2 to classify plant diseases from images with high accuracy.

## Features

- 🎯 **Accurate Detection**: Uses deep learning models to identify 25 different plant diseases across multiple crops
- 🌐 **Web Interface**: User-friendly web interface for uploading and analyzing plant images
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- ⚡ **Fast Predictions**: Quick image analysis and results
- 📊 **Confidence Scores**: Provides confidence levels for each prediction

## Supported Plants and Diseases

The model can detect diseases in the following plants:
- **Apple**: Scab, Black rot, Cedar apple rust, Healthy
- **Corn (Maize)**: Cercospora leaf spot, Common rust, Northern Leaf Blight, Healthy
- **Grape**: Black rot, Esca, Leaf blight, Healthy
- **Potato**: Early blight, Late blight, Healthy
- **Tomato**: Bacterial spot, Early blight, Late blight, Leaf Mold, Septoria leaf spot, Spider mites, Target Spot, Yellow Leaf Curl Virus, Mosaic virus, Healthy

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Hariprasath191/AgroVisionNet.git
cd AgroVisionNet
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

1. Start the Flask server:
```bash
python app.py
```

For development with debug mode:
```bash
FLASK_DEBUG=true python app.py
```

**Note**: Debug mode should NEVER be enabled in production as it poses a security risk.

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload a plant image and click "Analyze Plant" to get the disease detection results

### Training Your Own Model

If you have a plant disease dataset, you can train your own model:

```bash
python train_model.py --train-dir /path/to/training/data --epochs 10
```

Dataset structure should be:
```
training_data/
├── Apple___Apple_scab/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Apple___Black_rot/
│   └── ...
└── ...
```

### Command-Line Prediction

You can also make predictions from the command line:

```bash
python predict.py path/to/plant/image.jpg
```

## Project Structure

```
AgroVisionNet/
├── app.py                 # Flask web application
├── train_model.py         # Model training script
├── predict.py             # Command-line prediction script
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── uploads/          # Uploaded images
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
└── models/
    └── plant_disease_model.h5  # Trained model (created after training)
```

## API Endpoints

### GET /
Returns the main web interface

### POST /predict
Accepts an image file and returns disease prediction

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file with key "file"

**Response:**
```json
{
  "plant": "Tomato",
  "disease": "Early blight",
  "confidence": 95.67,
  "image_url": "/static/uploads/image.jpg",
  "message": "Prediction successful"
}
```

### GET /health
Returns the health status of the application

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Model Details

- **Architecture**: MobileNetV2 with transfer learning
- **Input Size**: 224x224 pixels
- **Output**: 25 disease classes
- **Framework**: TensorFlow/Keras

## Production Deployment

For production deployment, use a production-grade WSGI server instead of Flask's built-in server:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Security Recommendations:**
- Never enable debug mode in production
- Use HTTPS (SSL/TLS) for secure communication
- Implement rate limiting to prevent abuse
- Add authentication if needed
- Use environment variables for sensitive configuration
- Set up proper logging and monitoring

## Technologies Used

- **Backend**: Flask (Python web framework)
- **ML Framework**: TensorFlow/Keras
- **Model**: MobileNetV2 (Transfer Learning)
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: Pillow, NumPy

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Dataset: PlantVillage Dataset
- Pre-trained model: MobileNetV2 from TensorFlow/Keras
- Inspiration: Agricultural technology and AI for sustainable farming

## Contact

Hariprasath S. - [@Hariprasath191](https://github.com/Hariprasath191)

Project Link: [https://github.com/Hariprasath191/AgroVisionNet](https://github.com/Hariprasath191/AgroVisionNet)

## Future Enhancements

- [ ] Add more plant species and diseases
- [ ] Implement treatment recommendations
- [ ] Add multi-language support
- [ ] Create mobile app version
- [ ] Add disease severity assessment
- [ ] Implement user authentication
- [ ] Add history tracking for predictions
