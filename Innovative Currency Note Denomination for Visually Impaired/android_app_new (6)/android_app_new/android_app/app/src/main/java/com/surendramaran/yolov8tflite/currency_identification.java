package com.surendramaran.yolov8tflite;


import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class currency_identification extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_currency_identification);

        Button btnchange = findViewById(R.id.btn1);
        Button btnhistory = findViewById(R.id.btn2);

        // Handle English selection
        btnchange.setOnClickListener(v -> {
            goToChangeAppLanguagePage();

        });

        // Handle Hindi selection
        btnhistory.setOnClickListener(v -> {
            goToHistoryPage();

        });
    }


    // Navigate to the instruction page
    private void goToChangeAppLanguagePage() {
        Intent intent = new Intent(currency_identification.this, MainActivity.class);
        startActivity(intent);

    }
    private void goToHistoryPage() {
        Intent intent = new Intent(currency_identification.this, currency_counting.class);
        startActivity(intent);


    }
}
