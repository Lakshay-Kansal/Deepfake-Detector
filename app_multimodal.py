"""
Deepfake Detection Flask Backend
Supports BOTH Image and Audio Detection
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import librosa
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# =====================================================
# CONFIGURATION
# =====================================================
UPLOAD_FOLDER = 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a', 'ogg'}
MAX_FILE_SIZE = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =====================================================
# LOAD MODELS
# =====================================================
print("=" * 60)
print("🔄 Loading Detection Models...")
print("=" * 60)

# Load Image Model
IMAGE_MODEL = None
IMG_SIZE = 128

try:
    if os.path.exists('deepfake_detector_improved.h5'):
        IMAGE_MODEL = tf.keras.models.load_model('deepfake_detector_improved.h5')
        IMG_SIZE = 224
        print("✅ Image Model: deepfake_detector_improved.h5 (EfficientNet)")
    elif os.path.exists('deepfake_detector.h5'):
        IMAGE_MODEL = tf.keras.models.load_model('deepfake_detector.h5')
        IMG_SIZE = 128
        print("✅ Image Model: deepfake_detector.h5 (CNN)")
    elif os.path.exists('deepfake_detector.keras'):
        IMAGE_MODEL = tf.keras.models.load_model('deepfake_detector.keras')
        IMG_SIZE = 128
        print("✅ Image Model: deepfake_detector.keras")
    else:
        print("⚠️  No image model found - Image detection disabled")
except Exception as e:
    print(f"⚠️  Image model loading failed: {str(e)}")

# Load Audio Model
AUDIO_MODEL = None
AUDIO_MAX_LENGTH = 100

try:
    if os.path.exists('deepfake_audio_detector.h5'):
        AUDIO_MODEL = tf.keras.models.load_model('deepfake_audio_detector.h5')
        print("✅ Audio Model: deepfake_audio_detector.h5")
    elif os.path.exists('deepfake_audio_detector.keras'):
        AUDIO_MODEL = tf.keras.models.load_model('deepfake_audio_detector.keras')
        print("✅ Audio Model: deepfake_audio_detector.keras")
    else:
        print("⚠️  No audio model found - Audio detection disabled")
except Exception as e:
    print(f"⚠️  Audio model loading failed: {str(e)}")

print("=" * 60)
print(f"🎯 Available Features:")
print(f"   - Image Detection: {'✅ Enabled' if IMAGE_MODEL else '❌ Disabled'}")
print(f"   - Audio Detection: {'✅ Enabled' if AUDIO_MODEL else '❌ Disabled'}")
print("=" * 60 + "\n")

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def allowed_file(filename, file_type):
    """Check if file extension is allowed"""
    if not '.' in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'audio':
        return ext in ALLOWED_AUDIO_EXTENSIONS
    
    return False


def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Failed to read image")
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        
        return img
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")


def extract_audio_features(file_path, max_length=100):
    """Extract MFCC features from audio file"""
    try:
        # Load audio
        audio, sample_rate = librosa.load(file_path, duration=3.0, sr=22050)
        
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        
        # Pad or truncate
        if mfccs.shape[1] < max_length:
            pad_width = max_length - mfccs.shape[1]
            mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')
        else:
            mfccs = mfccs[:, :max_length]
        
        # Reshape for model
        mfccs = mfccs.reshape(1, mfccs.shape[0], mfccs.shape[1], 1)
        
        return mfccs
    except Exception as e:
        raise ValueError(f"Error processing audio: {str(e)}")


# =====================================================
# ROUTES
# =====================================================

@app.route('/')
def home():
    """Serve the main webpage"""
    return render_template('index.html')


@app.route('/predict/image', methods=['POST'])
def predict_image():
    """Handle image upload and prediction"""
    if IMAGE_MODEL is None:
        return jsonify({
            'success': False,
            'error': 'Image detection is not available. Model file missing.'
        }), 503
    
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, 'image'):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'
            }), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"📸 Processing image: {filename}")
        
        try:
            processed_image = preprocess_image(filepath)
        except ValueError as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'success': False, 'error': str(e)}), 400
        
        # Predict
        prediction = IMAGE_MODEL.predict(processed_image, verbose=0)[0][0]
        os.remove(filepath)
        
        # Interpret
        confidence = float(prediction)
        
        # Model output: closer to 1.0 = REAL, closer to 0.0 = FAKE
        is_real = confidence > 0.5
        label = "REAL" if is_real else "FAKE"
        real_probability = round(confidence * 100, 2)
        fake_probability = round((1 - confidence) * 100, 2)
        
        result = {
            'success': True,
            'type': 'image',
            'prediction': label,
            'confidence': round(confidence, 4),
            'fake_probability': fake_probability,
            'real_probability': real_probability
        }
        
        print(f"✅ Image Prediction: {label} (real={real_probability}%, fake={fake_probability}%)")
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/predict/audio', methods=['POST'])
def predict_audio():
    """Handle audio upload and prediction"""
    if AUDIO_MODEL is None:
        return jsonify({
            'success': False,
            'error': 'Audio detection is not available. Model file missing.'
        }), 503
    
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, 'audio'):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only WAV, MP3, FLAC, M4A, OGG allowed'
            }), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"🎵 Processing audio: {filename}")
        
        try:
            audio_features = extract_audio_features(filepath, AUDIO_MAX_LENGTH)
        except ValueError as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'success': False, 'error': str(e)}), 400
        
        # Predict
        prediction = AUDIO_MODEL.predict(audio_features, verbose=0)[0][0]
        os.remove(filepath)
        
        # Interpret
        confidence = float(prediction)
        
        # Model output: closer to 1.0 = REAL, closer to 0.0 = FAKE
        is_real = confidence > 0.5
        label = "REAL" if is_real else "FAKE"
        real_probability = round(confidence * 100, 2)
        fake_probability = round((1 - confidence) * 100, 2)
        
        result = {
            'success': True,
            'type': 'audio',
            'prediction': label,
            'confidence': round(confidence, 4),
            'fake_probability': fake_probability,
            'real_probability': real_probability
        }
        
        print(f"✅ Audio Prediction: {label} (real={real_probability}%, fake={fake_probability}%)")
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'features': {
            'image_detection': IMAGE_MODEL is not None,
            'audio_detection': AUDIO_MODEL is not None
        },
        'image_model_size': IMG_SIZE if IMAGE_MODEL else None,
        'audio_model_available': AUDIO_MODEL is not None
    }), 200


# =====================================================
# RUN APPLICATION
# =====================================================
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting Multi-Modal Deepfake Detection Server...")
    print("=" * 60)
    print("📍 Server: http://localhost:5000")
    print("💡 Press CTRL+C to stop")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
