package com.example.hazardui;

import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;
import com.example.hazardui.data.SoundObj;

import java.util.Objects;

public class HomeViewModel extends ViewModel {
    private static MutableLiveData<String> mText;
    private static MutableLiveData<Integer> mDistance;
    private static MutableLiveData<Integer> mColor;
    private static MutableLiveData<Integer> mDirection;
    private static MutableLiveData<Integer>[] mVisible;
    private static Handler handler;
    public HomeViewModel() {
        mText = new MutableLiveData<>();
        mDistance = new MutableLiveData<>();
        mColor = new MutableLiveData<>();
        mDirection= new MutableLiveData<>();
        mVisible = new MutableLiveData[8]; // Initialize the array
        handler = new Handler();

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

    public LiveData<Integer> getDirection() {
        return mDirection;
    }
    public LiveData<Integer>getVisibility(int i){
        return mVisible[i];
    }



    public void test_run () {
        mText.setValue("Siren");
        mDistance.setValue(2);
        mDirection.setValue(90); // Assuming you want to set a degree value
        mVisible[2].setValue(View.VISIBLE);
    }
    public static void doThings(BluetoothSocket socket, Context context){
        String input="";
        int SIZE=1024;
        byte[]buffer=new byte[SIZE];
//        Toast.makeText(context, "In Do Things",Toast.LENGTH_LONG).show();
        Log.e("doThings", "im in");
        while(!input.equals("end") && socket.isConnected())
        {
            try {
                //Log.e("Output", String.valueOf(socket.getOutputStream());
                //int byteCt = socket.getInputStream().read(buffer);**using socket buffer cleared it?

                //input= new String(buffer,0,byteCt);

                SoundObj inSound=null;
                int inDir= -1;
                int inDis = 0;
                try {
                    inSound = SoundObj.parseDelimitedFrom(socket.getInputStream());
                    //Log.e("Input", inSound.toString());
                }catch (Exception e){
                    Log.e("TEST","Error on logging parsed soundObj: "+e);
                }
                if(inSound!=null)
                {
                    input = inSound.getName();
                    inDis = inSound.getDistance();
                    inDir = inSound.getDirection();
                }
                else
                {
                    input="";
                }
                Log.e("INPUT",input);
                String finalInput = input;
                int finalInDir = inDir;
                SoundObj finalInSound = inSound;
                int finalInDis = inDis;
                handler.post(new Runnable() {
                    @Override
                    public void run() {
                        Log.e("run", "im in ");
                        mText.setValue(finalInput);
                        Log.e("mText1", Objects.requireNonNull(mText.getValue()));
                        mDirection.setValue(finalInDir);
                        mDistance.setValue(finalInDis);
                        if (mText.getValue().equals("Siren")) {
                            Log.e("COLOR","changed to red");
                            mColor.setValue(0xFFF44336);//red
                            mVisible[finalInDir].setValue(View.VISIBLE);
                        }
                        else {
                            for(int i=0;i<8;i++)
                                mVisible[i].setValue(View.INVISIBLE);

                            if(mText.getValue().equals("end")) {
                                mText.setValue("Disconnected");
                            }
                        }
                        //Log.e("LIST", history.toString());
                    }
                });
            }catch (Exception e){}
        }

    }
}
