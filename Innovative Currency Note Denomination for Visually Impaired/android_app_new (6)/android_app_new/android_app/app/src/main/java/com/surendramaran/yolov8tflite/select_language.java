package com.surendramaran.yolov8tflite;

import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class select_language extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select_language);

        Button buttonEnglish = findViewById(R.id.btnEnglish);
        Button buttonHindi = findViewById(R.id.btnHindi);

        // Handle English selection
        buttonEnglish.setOnClickListener(v -> {
            setLocale("en");  // Change the locale to English
            Toast.makeText(select_language.this, "You selected: English", Toast.LENGTH_SHORT).show();
            goToInstructionPage();
        });

        // Handle Hindi selection
        buttonHindi.setOnClickListener(v -> {
            setLocale("hi");  // Change the locale to Hindi
            Toast.makeText(select_language.this, "आपने चुना: हिन्दी", Toast.LENGTH_SHORT).show();
            goToInstructionPage();
        });
    }

    // Method to change the app's locale
    private void setLocale(String langCode) {
        Locale locale = new Locale(langCode);
        Locale.setDefault(locale);
        Configuration config = new Configuration();
        config.locale = locale;
        getResources().updateConfiguration(config, getResources().getDisplayMetrics());
    }

    // Navigate to the instruction page
    private void goToInstructionPage() {
        Intent intent = new Intent(select_language.this, front_page.class);
        startActivity(intent);
        finish();
    }
}
