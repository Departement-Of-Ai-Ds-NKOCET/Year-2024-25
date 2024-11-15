from flask import Flask, render_template, Response
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.applications import VGG16
import cv2
import joblib
import numpy as np

# Flask setup
app = Flask(__name__)

# Load feature extraction model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
feature_extractor = Model(inputs=base_model.input, outputs=GlobalAveragePooling2D()(base_model.output))

# Load pre-trained SVM classifier and scaler
svm_classifier = joblib.load('svm_classifier.pkl')
scaler = joblib.load('scaler.pkl')

# Function to predict dustiness
def predict_dustiness(image_array):
    # Preprocess input image
    image_array = np.expand_dims(image_array, axis=0) / 255.0
    
    # Extract features and predict dustiness
    features = feature_extractor.predict(image_array)
    features = scaler.transform(features)
    dust_prob = svm_classifier.predict_proba(features)[:, 1][0]
    return dust_prob

# Initialize video capture (use your webcam)
cap = cv2.VideoCapture(0)

# Function to generate frames for video streaming
def generate_video():
    while True:
        ret, frame = cap.read()  # Capture frame-by-frame
        if not ret:
            break
        
        # Resize the frame to match the model input size
        frame_resized = cv2.resize(frame, (128, 128))
        
        # Predict dustiness
        dust_prob = predict_dustiness(frame_resized)
        
        # Draw the dustiness probability on the frame
        cv2.putText(frame, f'Dustiness: {dust_prob:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Convert frame to JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)
        
        # Yield the frame in a format Flask can stream
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Route to display video stream
@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Index route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
