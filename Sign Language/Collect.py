import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

# Setup MediaPipe and parameters
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# # Configuration
# letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# num_samples_per_letter = 2000
# dataset = {letter: [] for letter in letters}
# collected_samples = {letter: num_samples_per_letter if letter <= 'P' else 0 for letter in letters}  # Skip A to P
# Configuration
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num_samples_per_letter = 2000
dataset = {letter: [] for letter in letters}
collected_samples = {letter: 0 for letter in letters}  # Initialize all letters to 0

# Helper functions
def draw_landmarks_and_bbox(image, hand_landmarks):
    # Draw hand landmarks
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    # Draw bounding box
    h, w, _ = image.shape
    x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
    y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
    x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
    y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)


def save_data(letter, landmarks):
    # Flatten landmarks into a single row
    row = np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark]).flatten()
    dataset[letter].append(row)


# Main data collection loop
cap = cv2.VideoCapture(0)
current_letter = None

print("Press 'ESC' to quit.")

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
            # Draw landmarks and bounding box
            draw_landmarks_and_bbox(frame, hand_landmarks)

            # Collect data if letter key is pressed
            if current_letter and collected_samples[current_letter] < num_samples_per_letter:
                save_data(current_letter, hand_landmarks)
                collected_samples[current_letter] += 1
                print(f"Collecting for {current_letter}: {collected_samples[current_letter]}/{num_samples_per_letter}")

                if collected_samples[current_letter] >= num_samples_per_letter:
                    print(f"Finished collecting for {current_letter}.")
                    current_letter = None  # Reset current letter

    # Show frame
    cv2.putText(frame, "Press a letter key to start collecting for that letter.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)
    cv2.imshow("Hand Landmarks", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key to quit
        break
    elif chr(key).upper() in letters:
        selected_letter = chr(key).upper()
        if collected_samples[selected_letter] < num_samples_per_letter:
            current_letter = selected_letter
            print(f"Started collecting for {current_letter}")

# Save dataset to CSV
for letter, data in dataset.items():
    if data:
        df = pd.DataFrame(data)
        df.to_csv(f'{letter}_dataset.csv', index=False)
        print(f"Saved {letter}_dataset.csv with {len(data)} samples.")

cap.release()
cv2.destroyAllWindows()
