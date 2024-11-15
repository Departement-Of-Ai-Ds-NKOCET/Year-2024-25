package com.surendramaran.yolov8tflite;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.Locale;

public class permission_page extends AppCompatActivity {

    private static final int PERMISSION_REQUEST_CODE = 123;
    private TextToSpeech textToSpeech;
    private String englishMessage = "Please give permission for camera and mic to scan Indian currency and record audio. Note: Only by allowing mic you will be able to put voice commands.";
    private String hindiMessage = "कृपया भारतीय मुद्रा स्कैन करने और ऑडियो रिकॉर्ड करने के लिए कैमरा और माइक्रोफोन की अनुमति दें। ध्यान दें: केवल माइक्रोफोन की अनुमति देकर ही आप वॉयस कमांड दे सकेंगे।";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_permission_page);

        // Initialize Text-to-Speech
        initializeTextToSpeech();
    }

    private void initializeTextToSpeech() {
        textToSpeech = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    // Set the language to English
                    int englishResult = textToSpeech.setLanguage(Locale.ENGLISH);
                    if (englishResult == TextToSpeech.LANG_MISSING_DATA || englishResult == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Toast.makeText(permission_page.this, "English language is not supported", Toast.LENGTH_SHORT).show();
                    } else {
                        // Set speech rate to normal (1.0 is default speed)
                        textToSpeech.setSpeechRate(1.0f);

                        // Start speaking immediately
                        speakMessages();
                    }
                } else {
                    Toast.makeText(permission_page.this, "Text-to-Speech Initialization failed", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void speakMessages() {
        // Speak the English message first
        textToSpeech.speak(englishMessage, TextToSpeech.QUEUE_FLUSH, null, "ENGLISH");

        // Monitor when the TTS finishes speaking English and then speak Hindi
        textToSpeech.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override
            public void onStart(String utteranceId) {}

            @Override
            public void onDone(String utteranceId) {
                if (utteranceId.equals("ENGLISH")) {
                    // Immediately set Hindi language and speak Hindi message
                    runOnUiThread(() -> {
                        int hindiResult = textToSpeech.setLanguage(new Locale("hi", "IN"));
                        if (hindiResult == TextToSpeech.LANG_MISSING_DATA || hindiResult == TextToSpeech.LANG_NOT_SUPPORTED) {
                            Toast.makeText(permission_page.this, "Hindi language is not supported", Toast.LENGTH_SHORT).show();
                        } else {
                            textToSpeech.speak(hindiMessage, TextToSpeech.QUEUE_FLUSH, null, "HINDI");
                        }
                    });
                } else if (utteranceId.equals("HINDI")) {
                    // After Hindi is done, request permissions immediately
                    checkAndRequestPermissions();
                }
            }

            @Override
            public void onError(String utteranceId) {}
        });
    }

    private void checkAndRequestPermissions() {
        // Check if Camera and Mic permissions are granted
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED ||
                ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            // Request the permissions if not granted
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.CAMERA, Manifest.permission.RECORD_AUDIO},
                    PERMISSION_REQUEST_CODE);
        } else {
            // If permissions are already granted, go to Welcome screen
            goToWelcomeScreen();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            // If permissions are granted, proceed to Welcome screen
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED &&
                    grantResults[1] == PackageManager.PERMISSION_GRANTED) {
                goToWelcomeScreen();
            } else {
                // Show a message if permissions are denied
                Toast.makeText(this, "Permissions are required to proceed.", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void goToWelcomeScreen() {
        // Go to Welcome screen after permissions are granted
        Intent welcomeIntent = new Intent(permission_page.this, welcome_page.class);
        startActivity(welcomeIntent);
        finish();
    }

    @Override
    protected void onDestroy() {
        // Shutdown TTS engine when the activity is destroyed
        if (textToSpeech != null) {
            textToSpeech.stop();
            textToSpeech.shutdown();
        }
        super.onDestroy();
    }
}
