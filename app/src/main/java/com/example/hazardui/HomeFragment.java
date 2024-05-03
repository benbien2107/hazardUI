package com.example.hazardui;

import android.graphics.Color;
import android.media.Image;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;


public class HomeFragment extends Fragment {
    HomeViewModel homeViewModel;
    TextView textView;
    ImageView[] signals;
    ImageView carImage;
    Animation blinkAnimation;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_home, container, false);
        homeViewModel = new ViewModelProvider(this).get(HomeViewModel.class);
        textView = view.findViewById(R.id.text_home);
        carImage = view.findViewById(R.id.car_img);
        signals = new ImageView[8];
        //zones = ["right", "front-right", "front", "front-left","left","back-left", "back", "back-right"]
        // go clockwise
        signals[0] = view.findViewById(R.id.triangle_right);
        signals[1] = view.findViewById(R.id.triangle_top_right);
        signals[2]= view.findViewById (R.id.triangle_top);
        signals[3] = view.findViewById(R.id.triangle_top_left);
        signals[4] = view.findViewById(R.id.triangle_left);
        signals[5] = view.findViewById(R.id.triangle_bottom_left);
        signals[6] = view.findViewById (R.id.triangle_bottom);
        signals[7] = view.findViewById(R.id.triangle_bottom_right);

        for (ImageView sig:signals) {
            sig.setVisibility(View.INVISIBLE);
        }

        manageDisplay();
        return view;
    }

    private void manageDisplay(){
//        homeViewModel.test_run();

        homeViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);


        homeViewModel.getDistance().observe(getViewLifecycleOwner(), new Observer<Integer>() {
            @Override
            public void onChanged(Integer distance) {
                int color;
                if (distance <= 1000) {
                    color = Color.RED;
                } else if (distance <= 5000) {
                    color = Color.YELLOW;
                } else {
                    color = Color.GREEN;
                }
                // Set the color to all signals
                for (ImageView signal : signals) {
                    signal.setColorFilter(color);
                }
            }
        });


        for (int i=0;i<signals.length;i++) {
            homeViewModel.getVisibility(i).observe(getViewLifecycleOwner(),signals[i]::setVisibility);
        }
    }
}