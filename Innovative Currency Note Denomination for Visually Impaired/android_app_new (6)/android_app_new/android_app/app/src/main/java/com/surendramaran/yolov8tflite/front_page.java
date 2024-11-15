package com.surendramaran.yolov8tflite;


import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class front_page extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_front_page); // Make sure this is the correct layout name

        // Initialize buttons
        Button btnCurrencyIdentification = findViewById(R.id.btn1);
        Button btnSettings = findViewById(R.id.btn2);

        // Set click listeners for the buttons
        btnCurrencyIdentification.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(front_page.this, "You selected Currency Identification", Toast.LENGTH_SHORT).show();
                openCurrencyIdentificationActivity(); // Open the Currency Identification activity
            }
        });

        btnSettings.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(front_page.this, "You selected Settings", Toast.LENGTH_SHORT).show();
                openSettingsActivity(); // Open the Settings activity
            }
        });
    }

    private void openCurrencyIdentificationActivity() {
        Intent intent = new Intent(front_page.this, currency_identification.class); // Replace with your Currency Identification activity
        startActivity(intent);
    }

    private void openSettingsActivity() {
        Intent intent = new Intent(front_page.this, settings.class); // Replace with your Settings activity
        startActivity(intent);
    }
}
