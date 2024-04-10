package com.example.hazardui;

import android.view.View;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class HomeViewModel extends ViewModel {
    private MutableLiveData<String> mText;
    private MutableLiveData<Integer> mDistance;
    private MutableLiveData<Integer> mColor;
    private MutableLiveData<Integer> mDegree;
    private MutableLiveData<Integer>[] mVisible;

    public HomeViewModel() {
        mText = new MutableLiveData<>();
        mDistance = new MutableLiveData<>();
        mColor = new MutableLiveData<>();
        mDegree = new MutableLiveData<>();
        mVisible = new MutableLiveData[8]; // Initialize the array

        for (int i = 0; i < mVisible.length; i++) {
            mVisible[i] = new MutableLiveData<>();
        }

        mText.setValue("Awaiting Connection...");
    }

    // Getter methods for LiveData objects

    public LiveData<String> getText() {
        return mText;
    }

    public LiveData<Integer> getDistance() {
        return mDistance;
    }

    public LiveData<Integer> getColor() {
        return mColor;
    }

    public LiveData<Integer> getDegree() {
        return mDegree;
    }
    public LiveData<Integer>getVisibility(int i){
        return mVisible[i];
    }

    public void test_run () {
        mText.setValue("Siren");
        mDistance.setValue(2);
        mDegree.setValue(90); // Assuming you want to set a degree value
        mVisible[2].setValue(View.VISIBLE);
    }
}
