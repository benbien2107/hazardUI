import pyaudio
import audioop
import threading
import signal
import time
import pandas as pd

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
FRAMES_PER_BUFFER = 1024
MIC_NAMES = ["Mic1", "Mic2"]
MIC_INDEX = 0 

# Lists for storing results:
framesMic1 = []   
framesMic2 = []
ampsMic1 = []
ampsMic2 = []
times = []

# Initialize PyAudio 
pa = pyaudio.PyAudio()

# One stream from the converter. 
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, 
                   input_device_index=MIC_INDEX, frames_per_buffer=FRAMES_PER_BUFFER)


# Function to record a stream
def record_mic(stream):
    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
    return data 

# Continuously record and store data 
def record_process(stop_signal):
    
    startTime = time.time() # Used to make time stamps

    while not stop_signal.is_set():
        # Set the time stamp
        timeStamp = time.time() - startTime
        
        # Record from device
        data = record_mic(stream)
        
        # Get the frames for each of the channels
        channel0 = data[0::CHANNELS]
        channel1 = data[1::CHANNELS]

        # Compute their amplitudes
        amp0 = audioop.rms(channel0, 2)
        amp1= audioop.rms(channel1, 2)

        # Print the results 
        print(f"Time: {timeStamp}\n\tMic1: {amp0}\n\tMic2: {amp1}\n")

        # Store the results
        framesMic1.append(channel0)     # Write frames
        framesMic2.append(channel1)

        ampsMic1.append(amp0)           # Write amplitudes
        ampsMic2.append(amp1)

        times.append(timeStamp)         # Write time stamps
        

# Write the frames to .wav file
def toWav(fName, frames):
    wf = wave.open(f'{fName}.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Write the time and amplitudes to Excel
def toExcel():
    col0 = "Timestamps"
    col1 = MIC_NAMES[0] + "Amplitude"
    col2 = MIC_NAMES[1] + 'Amplitude'
    df = pd.DataFrame( columns=[col0, col1, col2] )
    df.loc[col0] = times
    df.loc[col1] = ampsMic1
    df.loc[col2] = ampsMic2
    df.to_excel("amplitude_data.xlsx", index=False)

# Called after stop signal is given
def atEnd():
    # Close streams
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print("Recording stopped.")

    # Create .wav files and Excel file
    toWav(MIC_NAMES[0], framesMic1)
    toWav(MIC_NAMES[1], framesMic2)
    toExcel()
    print("Done writing files")


def signal_handler(signum, frame):
    stop_signal.set()

if __name__ == "__main__":
    stop_signal = threading.Event()
    signal.signal(signal.SIGINT, signal_handler)
    try:
        record_process(stop_signal)
    finally:
        atEnd() 