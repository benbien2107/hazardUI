import pyaudio
import wave
import audioop
import pandas as pd
from datetime import datetime
import threading
import signal


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1
FRAMES_PER_BUFFER = 1024
MIC_NAMES = ["Front Left", "Front Right", "Back Left", "Back Right"]

pa = pyaudio.PyAudio()

results_lock = threading.Lock()

def record_mic(device_index, record_seconds, results, index):
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=device_index, frames_per_buffer=FRAMES_PER_BUFFER)
    frames = []
    for _ in range(0, int(RATE / FRAMES_PER_BUFFER * record_seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
    stream.stop_stream()
    stream.close()

    filename = f"{MIC_NAMES[index]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    amplitude = audioop.rms(b''.join(frames), 2)
    
    with results_lock:
        results.append((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MIC_NAMES[index], amplitude))

def record_process(stop_signal, df):
    while not stop_signal.is_set():
        threads = []
        results = []
        for i in range(len(MIC_NAMES)):
            thread = threading.Thread(target=record_mic, args=(i, RECORD_SECONDS, results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for result in results:
            print(f"{result[1]}: Amplitude = {result[2]}")
            df.loc[len(df)] = result

def signal_handler(signum, frame):
    stop_signal.set()

if __name__ == "__main__":
    stop_signal = threading.Event()
    df = pd.DataFrame(columns=['Timestamp', 'Mic', 'Amplitude'])
    record_thread = threading.Thread(target=record_process, args=(stop_signal, df))
    signal.signal(signal.SIGINT, signal_handler)
    record_thread.start()
    record_thread.join()

    df.to_excel("amplitude_data.xlsx", index=False)
    pa.terminate()
    print("Recording stopped, data saved.")