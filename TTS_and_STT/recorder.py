import pyaudio
import wave
import keyboard

p = pyaudio.PyAudio()
inputKey="l" # push to talk button

# Settings
RATE = 16000
FORMAT = pyaudio.paInt16 # 16-bit frames, ie audio is in 2 bytes
CHANNELS = 1             # mono recording, use 2 if you want stereo
CHUNK_SIZE = 1024        # bytes


# Starts audio recording, on button release returns audio-file as path
def start_audio_input() ->str:
    if keyboard.is_pressed(inputKey):
        print("Recording")
        path: str ="education_bot/TTS_and_STT/recording.wav"
        with wave.open(path, "wb") as wavefile:
            p = pyaudio.PyAudio()
            wavefile.setnchannels(CHANNELS)
            wavefile.setsampwidth(p.get_sample_size(FORMAT))
            wavefile.setframerate(RATE)
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
            while keyboard.is_pressed(inputKey):
                wavefile.writeframes(stream.read(CHUNK_SIZE))
            print("End Recording")
            wavefile.close()
            stream.close()
            p.terminate
        
        return path
        
