import soundfile as sf
import pyaudio as pa

stream = pa.open(format=FORMAT, channels=4, rate=RATE, input=True, 
                 input_device_index=MIC_INDICES(i), frames_per_buffer=FRAMES_PER_BUFFER)
data = stream.read(FRAMES_PER_BUFFER)

channels = sf.read(data, channels=4)

# channels will be a tuple where each element is a numpy array representing a channel
channel_1, channel_2, channel_3, channel_4 = channels
