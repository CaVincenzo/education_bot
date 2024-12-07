import whisper
import pyaudio
import wave
import keyboard
import python_TTS

# Use push to Talk 'l' for voce request
# Use 'r' tu let request read out

model = whisper.load_model("tiny")
p = pyaudio.PyAudio()
inputKey="l"
python_TTS.init()

RATE = 16000
FORMAT = pyaudio.paInt16 # 16-bit frames, ie audio is in 2 bytes
CHANNELS = 1             # mono recording, use 2 if you want stereo
CHUNK_SIZE = 1024        # bytes

def startrecording():
    with wave.open("recording.wav", "wb") as wavefile:
        p = pyaudio.PyAudio()
        wavefile.setnchannels(CHANNELS)
        wavefile.setsampwidth(p.get_sample_size(FORMAT))
        wavefile.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
        for _ in range(0, RATE // CHUNK_SIZE * 5):
            wavefile.writeframes(stream.read(CHUNK_SIZE))
        wavefile.close()
        stream.close()
        p.terminate

# wisper 
def audioToString():
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio("education_bot/TTS_and_STT/recording.wav")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
  
    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    fileToWrite= "OUTPUT.txt"
    print(result.text)
    with open(fileToWrite, 'w') as file:
        file.write(result.text)
   
    return result.text

while True:
    if keyboard.is_pressed(inputKey):
        print("Recording")
        with wave.open("education_bot/TTS_and_STT/recording.wav", "wb") as wavefile:
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
        lastResult=audioToString()  
        
    #test TODO: Delete
    if keyboard.is_pressed('r'):
            print("Start Audio reading")
            python_TTS.audio_out("Starte test lesen")
            python_TTS.audio_out(audioToString())
