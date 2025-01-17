import pyaudio
import wave
import keyboard
import whisper

class AudioRecorder:
    def __init__(self, input_key_l='l',input_key_k='k', rate=16000, format=pyaudio.paInt16, channels=1, chunk_size=1024):
        """
        Initialisiert die AudioRecorder-Klasse mit den gewünschten Einstellungen.
        :param input_key: Taste für Push-to-Talk
        :param rate: Abtastrate (Hz)
        :param format: Audioformat (z. B. 16-Bit)
        :param channels: Anzahl der Kanäle (1 = Mono, 2 = Stereo)
        :param chunk_size: Größe der Audioblocks (Bytes)
        """
        self.p = pyaudio.PyAudio()
        self.input_key_l = input_key_l
        self.input_key_k = input_key_k
        self.rate = rate
        self.format = format
        self.channels = channels
        self.chunk_size = chunk_size
        self.whisper_model = whisper.load_model("base")  # Whisper-Modell laden
        
        
    def start_audio_input(self, output_path_l="recording_l.wav", output_path_k="recording_k.wav") -> str:
        """
        Startet die Audioaufnahme, solange die entsprechende Taste gedrückt wird.
        Gibt den Pfad zur aufgenommenen Audiodatei zurück.
        :param output_path_l: Pfad zur Ausgabedatei, wenn Taste 'l' gedrückt wird
        :param output_path_k: Pfad zur Ausgabedatei, wenn Taste 'k' gedrückt wird
        :return: Pfad der aufgenommenen Audiodatei oder None, wenn keine Taste gedrückt wurde
        """
        pressed_key = self.get_pressed_key()
        if not pressed_key:
            print("Keine gültige Taste gedrückt.")
            return None

        # Wähle den richtigen Ausgabe-Pfad basierend auf der gedrückten Taste
        output_path = output_path_l if pressed_key == self.input_key_l else output_path_k

        print(f"Recording gestartet für Taste '{pressed_key}'...")

        try:
            with wave.open(output_path, "wb") as wavefile:
                wavefile.setnchannels(self.channels)
                wavefile.setsampwidth(self.p.get_sample_size(self.format))
                wavefile.setframerate(self.rate)

                stream = self.p.open(format=self.format, 
                                    channels=self.channels, 
                                    rate=self.rate, 
                                    input=True)

                # Aufnahme läuft, solange die Taste gedrückt wird
                while keyboard.is_pressed(pressed_key):
                    wavefile.writeframes(stream.read(self.chunk_size))

                print("Recording beendet.")
                
                stream.stop_stream()
                stream.close()

            return output_path

        except Exception as e:
            print(f"Fehler während der Aufnahme: {e}")
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            return None


    # def start_audio_input(self, output_path_l="recording_l.wav",output_path_k="recording_k.wav") -> str:
    #     """
    #     Startet die Audioaufnahme, solange die Taste gedrückt wird. 
    #     Gibt den Pfad zur aufgenommenen Audiodatei zurück.
    #     :param output_path: Pfad zur Ausgabedatei
    #     :return: Pfad der Audiodatei
    #     """
    #     pressed_key = self.get_pressed_key()
    #     if not pressed_key:
    #         print("Keine gültige Taste gedrückt.")
    #         return None
        
    #     # Wähle den richtigen Ausgabe-Pfad basierend auf der gedrückten Taste
    #     output_path = output_path_l if pressed_key == self.input_key_l else output_path_k

    #     print(f"Recording gestartet für Taste '{pressed_key}'...")
        
    #     if keyboard.is_pressed(self.input_key_l):
    #         print("Recording...")
    #         with wave.open(output_path, "wb") as wavefile:
    #             wavefile.setnchannels(self.channels)
    #             wavefile.setsampwidth(self.p.get_sample_size(self.format))
    #             wavefile.setframerate(self.rate)

    #             stream = self.p.open(format=self.format, 
    #                                  channels=self.channels, 
    #                                  rate=self.rate, 
    #                                  input=True)

    #             while keyboard.is_pressed(self.input_key):
    #                 wavefile.writeframes(stream.read(self.chunk_size))

    #             print("End Recording")
                
    #             stream.stop_stream()
    #             wavefile.close()
    #             stream.close()

    #         return output_path
    
    def get_pressed_key(self):
        """
        Überprüft, ob eine der konfigurierten Tasten gedrückt wurde.
        :return: 'l' oder 'k', abhängig von der Taste, die gedrückt wurde, oder None, wenn keine Taste gedrückt ist.
        """
        if keyboard.is_pressed(self.input_key_l):
            return self.input_key_l
        if keyboard.is_pressed(self.input_key_k):
            return self.input_key_k
        return None

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
