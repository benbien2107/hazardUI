package com.example.hazardui;

import static androidx.constraintlayout.helper.widget.MotionEffect.TAG;


import static com.example.hazardui.HomeViewModel.doThings;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.Manifest;
import android.annotation.SuppressLint;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothServerSocket;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;


public class MainActivity extends AppCompatActivity {

    private HomeFragment homeFragment;
    private BluetoothAdapter bluetoothAdapter;
    private static final int SELECT_DEVICE_REQUEST_CODE = 2;
    private Handler handler;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        homeFragment = new HomeFragment();
        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
        fragmentTransaction.replace(R.id.frame_layout, homeFragment);
        fragmentTransaction.commit();
        BluetoothManager bluetoothManager = getSystemService(BluetoothManager.class);
        bluetoothAdapter = bluetoothManager.getAdapter();
        if (bluetoothAdapter == null) {
            Toast.makeText(this, "Bluetooth not supported", Toast.LENGTH_SHORT).show();// Device doesn't support Bluetooth
        }
        if (!bluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);

            Toast.makeText(this, "Bluetooth not enabled", Toast.LENGTH_SHORT).show();

            if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{android.Manifest.permission.BLUETOOTH_CONNECT}, SELECT_DEVICE_REQUEST_CODE);
            }
            startActivity(enableBtIntent);
            Toast.makeText(this, "Permission Granted", Toast.LENGTH_SHORT).show();
            finish();
        }
        requestPermissions(new String[]{Manifest.permission.BLUETOOTH_CONNECT}, SELECT_DEVICE_REQUEST_CODE);
        handler = new Handler();
        Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();
        ArrayList<String> pairedStr = new ArrayList<>();
        if (pairedDevices.size() > 0) {
            // There are paired devices. Get the name and address of each paired device.
            for (BluetoothDevice device : pairedDevices) {
                String deviceName = device.getName();
                String deviceHardwareAddress = device.getAddress();
                if(deviceName.equals("volgeorin-desktop"))//right now always accepts as long as name has been paired TODO
                {
                    Toast.makeText(this, "Found paired device: "+deviceName, Toast.LENGTH_SHORT).show();
                    (new AcceptThread()).start();
                    //Toast.makeText(this,"Continuing",Toast.LENGTH_SHORT).show();

                }
            }
        }
    }

    private class AcceptThread extends Thread {
        private final BluetoothServerSocket mmServerSocket;
        private final String NAME = "Test";
        private final UUID MY_UUID = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");

        @SuppressLint("MissingPermission")
        public AcceptThread() {

            // Use a temporary object that is later assigned to mmServerSocket
            // because mmServerSocket is final.
            BluetoothServerSocket tmp = null;
            //Toast.makeText(getApplicationContext(), "Listening for device \"connect()\"", Toast.LENGTH_SHORT).show();
            try {
                // MY_UUID is the app's UUID string, also used by the client code.
                tmp = bluetoothAdapter.listenUsingRfcommWithServiceRecord(NAME, MY_UUID);
            } catch (IOException e) {
                Log.e(TAG, "Socket's listen() method failed", e);
            }
            mmServerSocket = tmp;
        }

        public void run() {
            BluetoothSocket socket = null;
            // Keep listening until exception occurs or a socket is returned.
            while(socket==null||!socket.isConnected()){
                try {
                    Log.e("Socket", "Attempt to make socket");

                    //Toast.makeText(getApplicationContext(),"Attempt connect",Toast.LENGTH_LONG).show();
                    socket = mmServerSocket.accept();//device.createRfcommSocketToServiceRecord(UUID.fromString("0000110a-0000-1000-8000-00805f9b34fb"));
                    mmServerSocket.close();

                    if(socket!=null)
                    {
                        //Toast.makeText(getApplicationContext(), "Success! Connected", Toast.LENGTH_SHORT).show();
                        doThings(socket,getApplicationContext());//Method in HomeViewModel
                        socket.close();
                        Looper.prepare();
                        Toast.makeText(getApplicationContext(), "Disconnected",Toast.LENGTH_LONG).show();
                        break;
                    }

                } catch (IOException e) {
                    Log.e("Socket", "Attempt failed");
                    //Toast.makeText(getApplicationContext(),"Socket creation failed",Toast.LENGTH_SHORT).show();
                    e.printStackTrace();
                }
            }
        }

        // Closes the connect socket and causes the thread to finish.
        public void cancel() {
            try {
                mmServerSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "Could not close the connect socket", e);
            }
        }
    }

}
