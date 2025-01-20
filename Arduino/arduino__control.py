import serial
import time

class ArduinoController:
    def __init__(self, port='COM3', baud_rate=9600):
        """
        Initialisiert den ArduinoController mit den Verbindungsdetails.
        
        :param port: Der serielle Port, an dem der Arduino angeschlossen ist (z.B. 'COM3').
        :param baud_rate: Die Baudrate für die serielle Kommunikation (Standard: 9600).
        """
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self.baud_rate)
        time.sleep(2)  # Warten, bis die Verbindung hergestellt ist

    def wave(self):
        """
        Führt die Motorsteuerung durch (Starten und Stoppen).
        """
        # Drehen des Motors (Befehl 'D' senden)
        self.ser.write(b'D')  # Sende den Befehl 'D' an den Arduino (Motor startet)
        time.sleep(5)  # 5 Sekunden warten (Servo dreht sich)

        # Stoppen des Motors (Befehl 'S' senden)
        self.ser.write(b'S')  # Sende den Befehl 'S' an den Arduino (Motor stoppt)

        # Schließen der seriellen Verbindung
        self.ser.close()
