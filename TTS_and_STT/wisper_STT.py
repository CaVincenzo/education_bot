import whisper
from enum import Enum

# Use push to Talk 'l' for voce request


model = whisper.load_model("tiny")


# Comand Listen 
qNA_comands: list[str] = ["starte q and a", "q and a starte q and a", "abfrage starten"]
free_learning_comands: list[str] = ["starte freies lernen", "freises lernen starten"]
start_comands: list[str] = ["starte"]
bende_comands: list[str] = ["ende", "beende"]

comads= Enum ('comnad',[('starten',1),('benden',2),('qna',3)]) 

# wisper 
def audioToString(path:str) ->str:
    # load audio and pad/trim it to fit 30 seconds
    #audio = whisper.load_audio("education_bot/TTS_and_STT/recording.wav")
    audio = whisper.load_audio(path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    #_, probs = model.detect_language(mel)

    # decode the audio
    options = whisper.DecodingOptions(
        language="de",
        fp16=False,           # Verhindert die Nutzung von FP16 für genauere Berechnungen (wenn notwendig)
        beam_size=5,          # Höhere Beamgröße führt zu besseren Ergebnissen, aber langsamerer Verarbeitung
        best_of=5,            # Versucht 'best_of' der besten Ergebnisse (empfohlen bei leistungsstarken GPUs)
        temperature=0.0,      # Setzt die Temperatur auf 0 für deterministische Ergebnisse
        patience=1.0,         # Erhöht das Geduld-Verhältnis, um längere Zeit für das Decoding zu lassen
        length_penalty=1.0,   # Verhindert unnötig lange Ausgaben (kann verringert werden, wenn du lange Transkripte erwartest)
        suppress_blank=False, # Verhindert die Unterdrückung von "leeren" (Stille)-Tokens, wenn sie nicht notwendig sind
    )


    result = whisper.decode(model, mel, options)
    fileToWrite= "OUTPUT.txt"
    print(result.text)
    with open(fileToWrite, 'w') as file:
        file.write(result.text)
   
    return result.text

def is_a_comand(text:str, wordlist:list[str]) ->bool:
    value: bool = False
    for i in wordlist:
        if text.__contains__(i):# reconice Comand
            value = True
    
    return value
