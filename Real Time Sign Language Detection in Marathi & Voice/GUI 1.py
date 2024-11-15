import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from gtts import gTTS
import pygame
import os
import requests
import time
import tkinter as tk
from tkinter import Label, Button

# Load the trained model
model = load_model(r'E:\Sign Language\sign_language_model.h5')

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Alphabet labels
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
word = ""
translated_text = ""  # Variable to store the translated text

# Initialize pygame mixer
pygame.mixer.init()

# Function to preprocess landmarks for prediction
def preprocess_landmarks(hand_landmarks):
    landmark_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
    return landmark_array.reshape(1, -1)

# Function to translate text to Marathi
def translate_to_marathi(text):
    url = "https://api.mymemory.translated.net/get"
    params = {'q': text, 'langpair': 'en|mr'}
    response = requests.get(url, params=params)
    result = response.json()
    return result['responseData']['translatedText']

# Function to speak text using gTTS
def speak(text):
    try:
        filename = "temp_" + str(int(time.time())) + ".mp3"
        tts = gTTS(text=text, lang='mr')
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Error occurred while playing audio: {e}")
    finally:
        time.sleep(0.1)
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"Error deleting file: {e}")

# Update the GUI with the current detected letter and word
def update_gui():
    detected_label.config(text=f"Detected Letter: {last_detected_letter if last_detected_letter else ''}")
    word_label.config(text=f"Current Word: {word}")
    translated_label.config(text=f"Translated Sentence: {translated_text}")
    root.after(100, update_gui)  # Update GUI every 100ms

# Define button functions
def add_space():
    global word
    word += ' '

def delete_last_letter():
    global word
    word = word[:-1]

def clear_word():
    global word
    word = ""

def translate_word():
    global translated_text
    translated_text = translate_to_marathi(word)

def voice_translation():
    global translated_text
    # Check if translation exists, otherwise translate before speaking
    if not translated_text:
        translate_word()
    speak(translated_text)

# Initialize variables for detection
cap = cv2.VideoCapture(0)
last_detected_letter = None
last_detection_time = 0  # Initialize to 0 to ensure it has a value at start
detection_delay = 1.5

# Create the main GUI window
root = tk.Tk()
root.title("Sign Language Detection GUI")

# Left-aligned labels for detected text
detected_label = Label(root, text="Detected Letter: ", font=("Arial", 14))
detected_label.pack(anchor='w', padx=10, pady=(10, 0))

word_label = Label(root, text="Current Word: ", font=("Arial", 14))
word_label.pack(anchor='w', padx=10, pady=(5, 0))

translated_label = Label(root, text="Translated Sentence: ", font=("Arial", 14))
translated_label.pack(anchor='w', padx=10, pady=(5, 10))

# Frame to organize buttons in a single line
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Buttons for the actions, arranged horizontally
space_button = Button(button_frame, text="Space", command=add_space, font=("Arial", 12))
space_button.pack(side="left", padx=5)

delete_button = Button(button_frame, text="Delete Last", command=delete_last_letter, font=("Arial", 12))
delete_button.pack(side="left", padx=5)

clear_button = Button(button_frame, text="Clear Word", command=clear_word, font=("Arial", 12))
clear_button.pack(side="left", padx=5)

translate_button = Button(button_frame, text="Translate", command=translate_word, font=("Arial", 12))
translate_button.pack(side="left", padx=5)

voice_button = Button(button_frame, text="Voice", command=voice_translation, font=("Arial", 12))
voice_button.pack(side="left", padx=5)

# Run the GUI updates in a loop
update_gui()

# Start capturing video frames
def video_loop():
    global last_detected_letter, word, last_detection_time  # Make last_detection_time global
    ret, frame = cap.read()
    if not ret:
        root.quit()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = preprocess_landmarks(hand_landmarks)
            prediction = model.predict(landmarks)
            predicted_letter = letters[np.argmax(prediction)]
            confidence = np.max(prediction)
            current_time = time.time()
            if confidence > 0.7 and (current_time - last_detection_time) > detection_delay:
                last_detected_letter = predicted_letter
                word += last_detected_letter
                last_detection_time = current_time  # Update last detection time
            cv2.putText(frame, f"Detected: {last_detected_letter}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Webcam", frame)
    root.after(10, video_loop)  # Update the video feed every 10ms

# Start the video loop
video_loop()

# Main loop
root.mainloop()

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
