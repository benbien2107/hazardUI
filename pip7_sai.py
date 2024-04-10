import pyaudio
import audioop
import threading
import signal

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1
FRAMES_PER_BUFFER = 1024
MIC_NAMES = ["Set1", "Set2","Set3", "Set4"]
MIC_INDEX = [25, 26, 27, 28]

pa = pyaudio.PyAudio()

def record(stream, mic_name, results):
    one_second_frames = []
    for i in range(0, int(RATE/FRAMES_PER_BUFFER)):
        frames = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
        one_second_frames.append(frames)
    amplitude = audioop.rms(b''.join(one_second_frames), 2)
    results.append((mic_name, amplitude))

def start(stop_signal):
    streams = [pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=MIC_INDEX[i], frames_per_buffer=FRAMES_PER_BUFFER) for i in range(len(MIC_INDEX))]
    contin_record(stop_signal, streams)

def contin_record(stop_signal, streams):
        try:
            while not stop_signal.is_set():
                results = []
                for i, stream in enumerate(streams):
                    record(stream, MIC_NAMES[i], results)

                highest_amplitude = max(results, key=lambda item: item[1])
                for result in results:
                    print(f"{result[0]}: Amplitude = {result[1]}")
                print(f"Highest Amplitude Mic: {highest_amplitude[0]} Amplitude = {highest_amplitude[1]}")

        finally:
            for stream in streams:
                stream.stop_stream()
                stream.close()
            pa.terminate()

def signal_handler(signum, frame):
    stop_signal.set()

if __name__ == "__main__":
    stop_signal = threading.Event()
    signal.signal(signal.SIGINT, signal_handler)

    start(stop_signal)
    print("Recording stopped.")
