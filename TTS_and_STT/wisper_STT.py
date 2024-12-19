import whisper


# Use push to Talk 'l' for voce request


model = whisper.load_model("tiny")

# wisper 
def audioToString(path:str) ->str:
    # load audio and pad/trim it to fit 30 seconds
    #audio = whisper.load_audio("education_bot/TTS_and_STT/recording.wav")
    audio = whisper.load_audio(path)
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

