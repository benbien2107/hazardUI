import pyaudio
import audioop
import threading
import signal
from gaussNewton import gaussNewton, toPolarCoords

'''
This file adds the Gauss-Newton Method to our direction finding pipeline. Specifically, to pip5.py
'''

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1
FRAMES_PER_BUFFER = 1024
MIC_NAMES = ["Set1", "Set2","Set3", "Set4"]
MIC_INDEX = [25,26,27,28]
MIC_CENTERS = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
Max_Amp_Index = 0

pa = pyaudio.PyAudio()


# create 1 thread for frames and 1 thread for 1 second chuncks 
def record(stream, mic_name, results, amps, frames_1s):
    frames = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
    frames_1s.append(frames)
    amplitude = audioop.rms(frames, 2)
    results.append((mic_name, amplitude))
    amps.append(amplitude)
    
def record(stop_signal, stream, mic_name, results, amps, frames_1s):
    while not stop_signal.is_set():
        frame = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
        frames_1s.append(frame)

        thread = threading.Thread(target=process_frame, args=(frame, mic_name, results, amps))
        thread.start()

    thread = threading.Thread(target=process_chunk, args=(frames_1s,))
    thread.start()


def start(stop_signal):
    threads = []
    for i in range(len(MIC_INDEX)):
        stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                         input_device_index=MIC_INDEX[i], frames_per_buffer=FRAMES_PER_BUFFER)
        thread = threading.Thread(target=contin_record, args=(stop_signal,stream))
        thread.start()
        threads.append(thread)
        
    for thread in threads:
        thread.join()

def useGaussNewton(highest_amplitude, amplitudes):
    # Get the index of the max amplitude
    max_amp_index = MIC_NAMES.index(highest_amplitude[0])
    # Use the center of the mic with the max as the initial x, y
    initial_x, initial_y = MIC_CENTERS[max_amp_index]
    # Store the initial values, let k = 1. 
    ivs = [initial_x, initial_y, 1]
    # Get the approximated location
    x, y, k = gaussNewton(amplitudes, MIC_CENTERS, ivs, tol=1e-3, maxSteps=10)
    # Convert to polar coordinates, we can use theta to show the direction on a unit circle
    r, theta = toPolarCoords(x, y)
    # Print output for now
    print(f"Max Direction: x = {x}, y = {y}")
    return (r, theta)



def contin_record(stop_signal, stream):
    frames_1s = []
    counter = 0
    try:
        while not stop_signal.is_set():
            results = []
            amps = []
            record(stream, MIC_NAMES[MIC_INDEX.index(stream.get_input_device())], results, amps, frames_1s)
            counter += 1

            if counter >= RATE / FRAMES_PER_BUFFER:  # We have 1 second stored
                counter = 0
                print("1s of Frames stored", frames_1s)  # Print the frames in 1s
                frames_1s = []

            highest_amplitude = max(results, key=lambda item: item[1])

            r, theta = useGaussNewton(highest_amplitude, amps)

            for result in results:
                print(f"{result[0]}: Amplitude = {result[1]}")
            print(f"Highest Amplitude Mic: {highest_amplitude[0]} Amplitude = {highest_amplitude[1]}")

    finally:
        stream.stop_stream()
        stream.close()

def signal_handler(signum, frame):
    stop_signal.set()

if __name__ == "__main__":
    stop_signal = threading.Event()
    signal.signal(signal.SIGINT, signal_handler)

    start(stop_signal)
    print("Recording stopped.")

