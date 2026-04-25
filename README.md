# 🔍 Deepfake Detection Web Application

A full-stack web application that uses a CNN model to detect deepfake images. Built with TensorFlow, Flask, and vanilla JavaScript.

## 📋 Features

- Upload images via drag-and-drop or file picker
- Real-time deepfake detection using trained CNN model
- Confidence score visualization
- Clean, modern UI with responsive design
- Support for PNG, JPG, JPEG formats

## 🛠️ Technologies Used

**Backend:**
- Flask (Python web framework)
- TensorFlow/Keras (ML model)
- OpenCV (Image processing)
- Flask-CORS (Cross-origin support)

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Responsive design

**Machine Learning:**
- CNN architecture (Conv2D, MaxPooling, Dense layers)
- Binary classification (Real vs Fake)
- Image preprocessing (128x128, normalization)

## 📁 Project Structure

```
deepfake-detector/
├── app.py                      # Flask backend
├── deepfake_detector.h5        # Trained model
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Frontend UI
├── uploads/                   # Temporary upload folder (auto-created)
└── README.md                  # Documentation
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd deepfake-detector
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure your trained model is present**
   - Make sure `deepfake_detector.h5` is in the project root directory
   - This is the model you trained using the CNN notebook

## ▶️ Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   - Navigate to: `http://localhost:5000`
   - Or: `http://127.0.0.1:5000`

3. **Upload and test**
   - Drag and drop an image or click to upload
   - Click "Analyze Image"
   - View the results!

## 📊 How It Works

### Backend Flow
1. User uploads image via frontend
2. Flask receives POST request with image file
3. Image is saved temporarily and preprocessed:
   - Resized to 128x128 pixels
   - Normalized (0-1 range)
   - Batch dimension added
4. Model makes prediction
5. Results sent back as JSON
6. Temporary file deleted

### Model Architecture
```
Conv2D (32 filters) → MaxPooling → 
Conv2D (64 filters) → MaxPooling → 
Conv2D (128 filters) → MaxPooling → 
Flatten → Dense (128) → Dropout → 
Dense (1, sigmoid)
```

### API Endpoints

**POST /predict**
- Upload image for analysis
- Returns: `{prediction, confidence, fake_probability, real_probability}`

**GET /health**
- Check server status
- Returns: `{status, model_loaded}`

## 🎨 Frontend Features

- **Drag & Drop**: Easy file upload
- **Live Preview**: See uploaded image before analysis
- **Loading State**: Visual feedback during processing
- **Color-Coded Results**: 
  - Green for REAL images
  - Red for FAKE images
- **Confidence Bar**: Visual representation of certainty
- **Error Handling**: User-friendly error messages

## 🔧 Troubleshooting

**Model not found error:**
- Ensure `deepfake_detector.h5` is in the same directory as `app.py`

**Port already in use:**
- Change the port in `app.py`: `app.run(port=5001)`

**CORS errors:**
- Flask-CORS is already configured, ensure it's installed

**Upload errors:**
- Check file size (max 16MB)
- Verify file format (PNG, JPG, JPEG only)

## 📈 Potential Improvements

- [ ] Add video support (frame-by-frame analysis)
- [ ] Implement batch processing
- [ ] Add user authentication
- [ ] Store analysis history in database
- [ ] Deploy to cloud (Heroku, Render, AWS)
- [ ] Add more detailed heatmap visualizations
- [ ] Implement model versioning
- [ ] Add API rate limiting

## 📝 Model Performance

- **Training Accuracy**: ~XX% (add your results)
- **Test Accuracy**: ~XX% (add your results)
- **Dataset**: Kaggle Deepfake and Real Images
- **Training Time**: ~XX minutes (add your results)

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ CNN model training for image classification
- ✅ Flask API development
- ✅ File upload handling
- ✅ Frontend-backend integration
- ✅ Model deployment and inference
- ✅ Error handling and validation
- ✅ Responsive web design

## 📄 License

This is a college project for educational purposes.

## 👥 Contributors

[Add your name and details]

## 🙏 Acknowledgments

- Kaggle for the deepfake dataset
- TensorFlow/Keras documentation
- Flask documentation
