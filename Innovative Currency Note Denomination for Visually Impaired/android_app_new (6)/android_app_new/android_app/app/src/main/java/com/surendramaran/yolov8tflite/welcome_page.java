package com.surendramaran.yolov8tflite;

import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.Locale;

public class welcome_page extends AppCompatActivity {
    private TextToSpeech textToSpeech;
    private String welcomeMessageEnglish = "Welcome to TRINETRA Application. You can choose language for app from out of 2 available languages. Note: denomination of the note will be in same language";
    private String welcomeMessageHindi = "त्रिनेत्रा एप्लिकेशन में आपका स्वागत है। आप एप्लिकेशन के लिए 2 उपलब्ध भाषाओं में से कोई भी भाषा चुन सकते हैं।  ध्यान दें: नोट का मूल्यांकन (मूल्य) उसी भाषा में होगा।";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome_page); // Set your welcome layout

        // Initialize Text-to-Speech
        initializeTextToSpeech();

        // Button to select language
        Button selectLanguageButton = findViewById(R.id.btn1);
        selectLanguageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Start the SelectLanguageActivity when the button is clicked
                Intent intent = new Intent(welcome_page.this, select_language.class);
                startActivity(intent);
            }
        });
    }

    private void initializeTextToSpeech() {
        textToSpeech = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    // Set the language to English first
                    int englishResult = textToSpeech.setLanguage(Locale.ENGLISH);
                    if (englishResult == TextToSpeech.LANG_MISSING_DATA || englishResult == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Toast.makeText(welcome_page.this, "English language is not supported", Toast.LENGTH_SHORT).show();
                    } else {
                        // Start speaking English and then Hindi
                        speakEnglishThenHindi();
                    }
                } else {
                    Toast.makeText(welcome_page.this, "Text-to-Speech Initialization failed", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void speakEnglishThenHindi() {
        // Speak the welcome message in English first
        textToSpeech.speak(welcomeMessageEnglish, TextToSpeech.QUEUE_FLUSH, new Bundle(), "ENGLISH_WELCOME");

        // Monitor the TTS progress to handle language switching
        textToSpeech.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override
            public void onStart(String utteranceId) {}

            @Override
            public void onDone(String utteranceId) {
                if (utteranceId.equals("ENGLISH_WELCOME")) {
                    // After English, set Hindi language
                    int hindiResult = textToSpeech.setLanguage(new Locale("hi", "IN"));
                    if (hindiResult == TextToSpeech.LANG_MISSING_DATA || hindiResult == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Toast.makeText(welcome_page.this, "Hindi language is not supported", Toast.LENGTH_SHORT).show();
                    } else {
                        // Speak the welcome message in Hindi
                        textToSpeech.speak(welcomeMessageHindi, TextToSpeech.QUEUE_FLUSH, new Bundle(), "HINDI_WELCOME");
                    }
                }
            }

            @Override
            public void onError(String utteranceId) {}
        });
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
