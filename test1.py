import pyaudio
import wave
import audioop
import pandas as pd
from datetime import datetime
import threading
import signal

FORMAT = pyaudio.paInt16
CHANNELS = 4  # Number of channels
RATE = 44100
RECORD_SECONDS = 1
FRAMES_PER_BUFFER = 1024
MIC_NAMES = ["Front Left", "Front Right", "Back Left", "Back Right"]

pa = pyaudio.PyAudio()

results_lock = threading.Lock()


# Write the frames to .wav file
def toWav(fName, frames):
    wf = wave.open(f'{fName}.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def record_process(stop_signal, df):
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)

    while not stop_signal.is_set():
        frames = []
        for _ in range(0, int(RATE / FRAMES_PER_BUFFER * RECORD_SECONDS)):
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data) # this is for the 44 frames aka 1 second chunk ( we can techniquely go for each frames direction (1024) now since of slicing)

        # De-interleave the audio data into separate channels ( 1 second chunk)
        channels_data = [frames[i::CHANNELS] for i in range(CHANNELS)]
        # Calculate amplitude for each channel
        amplitudes = [audioop.rms(b''.join(channel_data), 2) for channel_data in channels_data]
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i, mic_name in enumerate(MIC_NAMES):
            print(f"{mic_name}: Amplitude = {amplitudes[i]}")
           
                
    for i, mic_name in enumerate(MIC_NAMES):
        filename = f"{MIC_NAMES[i]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        toWav(filename,channels_data[i])

    stream.stop_stream()
    stream.close()

def signal_handler(signum, frame):
    stop_signal.set()

if __name__ == "__main__":
    stop_signal = threading.Event()

    record_thread = threading.Thread(target=record_process, args=(stop_signal, df))
    signal.signal(signal.SIGINT, signal_handler)
    record_thread.start()
    record_thread.join()
    pa.terminate()
    print("Recording stopped, data saved.")
