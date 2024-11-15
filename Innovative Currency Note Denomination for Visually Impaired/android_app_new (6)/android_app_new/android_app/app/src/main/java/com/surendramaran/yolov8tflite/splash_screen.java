package com.surendramaran.yolov8tflite;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import androidx.appcompat.app.AppCompatActivity;

public class splash_screen extends AppCompatActivity {

    private static final int SPLASH_DELAY = 2000; // 2 seconds

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash_screen);

        // Initialize SharedPreferences to check if it's the first run
        SharedPreferences preferences = getSharedPreferences("AppPrefs", MODE_PRIVATE);
        boolean isFirstRun = preferences.getBoolean("isFirstRun", true);

        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            if (isFirstRun) {
                // Set isFirstRun to false so it doesn't run this logic next time
                SharedPreferences.Editor editor = preferences.edit();
                editor.putBoolean("isFirstRun", false);
                editor.apply();

                // Navigate through first-time flow
                navigateToPermissionPage();
            } else {
                // Navigate directly to the front page
                navigateToFrontPage();
            }
        }, SPLASH_DELAY);
    }

    private void navigateToPermissionPage() {
        Intent intent = new Intent(splash_screen.this, permission_page.class);
        startActivity(intent);
        finish();
    }

    private void navigateToFrontPage() {
        Intent intent = new Intent(splash_screen.this, front_page.class);
        startActivity(intent);
        finish();
    }
}
