import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
# model = load_model('E:\2000 Samples\sign_language_model.h5')  # Update this with the actual path
model = load_model(r'E:\Sign Language\sign_language_model.h5')
# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Alphabet labels
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# Helper function to preprocess landmarks for prediction
def preprocess_landmarks(hand_landmarks):
    # Flatten the landmark coordinates into a 1D array
    landmark_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
    return landmark_array.reshape(1, -1)


# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Prepare landmarks for prediction
            landmarks = preprocess_landmarks(hand_landmarks)

            # Make prediction
            prediction = model.predict(landmarks)
            predicted_letter = letters[np.argmax(prediction)]
            confidence = np.max(prediction)

            # Display the predicted letter on the screen if confidence is above a threshold
            if confidence > 0.7:
                cv2.putText(frame, f"Prediction: {predicted_letter} ({confidence:.2f})", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow("Sign Language Detection", frame)

    # Exit loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
