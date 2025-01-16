import pyaudio
import wave
import keyboard
import whisper

class AudioRecorder:
    def __init__(self, input_key="l", rate=16000, format=pyaudio.paInt16, channels=1, chunk_size=1024):
        """
        Initialisiert die AudioRecorder-Klasse mit den gewünschten Einstellungen.
        :param input_key: Taste für Push-to-Talk
        :param rate: Abtastrate (Hz)
        :param format: Audioformat (z. B. 16-Bit)
        :param channels: Anzahl der Kanäle (1 = Mono, 2 = Stereo)
        :param chunk_size: Größe der Audioblocks (Bytes)
        """
        self.p = pyaudio.PyAudio()
        self.input_key = input_key
        self.rate = rate
        self.format = format
        self.channels = channels
        self.chunk_size = chunk_size
        self.whisper_model = whisper.load_model("base")  # Whisper-Modell laden

    def start_audio_input(self, output_path="recording.wav") -> str:
        """
        Startet die Audioaufnahme, solange die Taste gedrückt wird. 
        Gibt den Pfad zur aufgenommenen Audiodatei zurück.
        :param output_path: Pfad zur Ausgabedatei
        :return: Pfad der Audiodatei
        """
        if keyboard.is_pressed(self.input_key):
            print("Recording...")
            with wave.open(output_path, "wb") as wavefile:
                wavefile.setnchannels(self.channels)
                wavefile.setsampwidth(self.p.get_sample_size(self.format))
                wavefile.setframerate(self.rate)

                stream = self.p.open(format=self.format, 
                                     channels=self.channels, 
                                     rate=self.rate, 
                                     input=True)

                while keyboard.is_pressed(self.input_key):
                    wavefile.writeframes(stream.read(self.chunk_size))

                print("End Recording")
                
                stream.stop_stream()
                wavefile.close()
                stream.close()

            return output_path

    def transcribe_with_whisper(self, audio_file_path: str) -> str:
        """
        Transkribiert die angegebene Audiodatei mit Whisper.
        :param audio_file_path: Pfad zur Audiodatei.
        :return: Transkribierter Text.
        """
        print("Transcribing audio with Whisper...")
        result = self.whisper_model.transcribe(audio_file_path)
        return result.get("text", "").strip()

    def close(self):
        """
        Beendet PyAudio.
        """
        self.p.terminate()
