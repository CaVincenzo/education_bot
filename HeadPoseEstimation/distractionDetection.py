import os
import random
import sys
import cv2
from ultralytics import YOLO
from PIL import Image
import numpy as np
import math
import time
from pylips.speech import RobotFace

# Füge das Hauptverzeichnis zum Modulpfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Arduino.arduino__control import ArduinoController


interrupt = False
face = RobotFace()  
arduino = ArduinoController(port='COM3', baud_rate=9600)

global focus
FocusCounter = 0

def focus_check():
    
    global FocusCounter 
    
    if not focus:
        FocusCounter += 1
        print("Warnung: Der Benutzer ist abgelenkt!")
        
        if FocusCounter == 2:
            print("Winken.")
            arduino.wave()
            
        elif FocusCounter == 3:
            print("Der Benutzer ist abgelenkt.")
            motivational_sentence = get_random_motivational_sentence()
            face.say(motivational_sentence)
            face.wait()
            
        elif FocusCounter > 3 and FocusCounter % 2 != 0:
            print("Der Benutzer ist abgelenkt.")
            motivational_sentence = get_random_motivational_sentence()
            face.say(motivational_sentence)
            face.wait()
    else:
        print("Der Benutzer ist fokussiert.")
        FocusCounter = 0


def get_random_motivational_sentence():
    motivational_sentences = [
        "Hey, ich weiß, es ist schwer, aber ich glaube an dich – du kannst das schaffen!",
        "Ich weiß, wie weit du schon gekommen bist, also nimm dir einen Moment, atme durch und mach weiter.",
        "Manchmal brauchst du nur einen kleinen Neustart – fang einfach hier und jetzt an.",
        "Du bist so schlau und stark – diese Aufgabe hat keine Chance gegen dich.",
        "Komm, wir machen das zusammen: ein Schritt nach dem anderen, okay?",
        "Du hast schon so viel gelernt. Stell dir vor, wie stolz du auf dich sein wirst, wenn du weitermachst!",
        "Es ist okay, eine Pause zu machen, aber gib nicht auf. Ich bin hier und glaube an dich.",
        "Denk daran, warum du angefangen hast – du verdienst es, dein Ziel zu erreichen.",
        "Du bist genau da, wo du sein sollst, und ich bin so stolz auf deinen Einsatz.",
        "Vergiss nicht: Selbst kleine Fortschritte sind Fortschritte. Und du machst das großartig!"
    ]
    return random.choice(motivational_sentences)

def capture_image(output_path="testCapturedImage.png"):
    """Funktion zum Aufnehmen eines Bildes mit der Webcam."""
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    # Lesen des Eingabebildes von der Kamera
    result, image = cam.read()

    if result:
        # Bild speichern
        cv2.imwrite(output_path, image)
        return output_path
    else:
        print("Kein Bild erkannt. Bitte versuchen Sie es erneut.")
        return None

def analyze_image_with_yolo(image_path):
    """Funktion zur Analyse eines Bildes mit YOLO."""
    model = YOLO("yolo11l-pose.pt")

    # Bild mit YOLO verarbeiten
    results = model(image_path)
    try:
        # Koordinaten der Gesichtspunkte extrahieren
        keypoints = results[0].keypoints.xy.numpy()  # Konvertiere zu NumPy-Array
        nose = np.array([keypoints[0][0][0], keypoints[0][0][1]])  # x, y der Nase
        left_eye = np.array([keypoints[0][1][0], keypoints[0][1][1]])  # x, y des linken Auges
        right_eye = np.array([keypoints[0][2][0], keypoints[0][2][1]])  # x, y des rechten Auges

        # Mittelpunkt der Augen berechnen
        eye_center_x = (left_eye[0] + right_eye[0]) / 2
        eye_center_y = (left_eye[1] + right_eye[1]) / 2

        # Differenzen berechnen
        dx = nose[0] - eye_center_x
        dy = nose[1] - eye_center_y

        # Winkel in Grad berechnen
        yaw_angle = (math.atan2(dy, dx) * (180 / math.pi)) - 90

        return yaw_angle
    except:
        return None
        

def setup():
    #Setup-Funktion zur Aufnahme der Links- und Rechts-Winkel.
    print("Setup: Wir werden die Winkel für links und rechts aufnehmen.")
    face.say(" Für die Kalibrierung schaue nach Aufforderung an den linken und rechten Rand deines Arbeitsbereiches.")
    face.wait()
    print("Bitte nach links schauen.")
    face.say("Bitte nach links schauen.")
    face.wait()
    time.sleep(2)
    
    left_image_path = capture_image("left_view.png")
    if not left_image_path:
        print("Fehler beim Aufnehmen des linken Bildes.")
        face.say("Fehler beim Aufnehmen des linken Bildes.")
        face.wait()
        return None, None
    left_angle = analyze_image_with_yolo(left_image_path)
    
    if left_angle == None:
        return None, None

    print("Bitte nach rechts schauen.")
    face.say("Bitte nach rechts schauen.")
    face.wait()
    time.sleep(2)
    
    right_image_path = capture_image("right_view.png")
    if not right_image_path:
        print("Fehler beim Aufnehmen des rechten Bildes.")
        face.say("Fehler beim Aufnehmen des rechten Bildes.")  
        face.wait()
        return None, None
    right_angle = analyze_image_with_yolo(right_image_path)
    
    face.say("Kalibrierung abgeschlossen.")
    face.wait()
    face.say("Viel spaß beim freien lernen.")
    face.wait()

    return left_angle, right_angle

def monitor_angles(left_angle, right_angle):
    global focus
    
    print("Neues Bild wird aufgenommen...")
    current_image_path = capture_image("current_view.png")
    if not current_image_path:
        print("Fehler beim Aufnehmen des aktuellen Bildes.")
    current_angle = analyze_image_with_yolo(current_image_path)
    
    if current_angle == None:
        print("Warnung: Blickwinkel konnte nicht erfasst werden!")
        focus = False
    elif current_angle > right_angle:
        print("Warnung: Person schaut weiter nach rechts als im Setup angegeben!")
        focus = False
    elif current_angle < left_angle:
        print("Warnung: Person schaut weiter nach links als im Setup angegeben!")
        focus = False
    else:
        print("Blickwinkel ist innerhalb des zulässigen Bereichs.")
        focus = True

def monitor(left_angle, right_angle):
    """Funktion zur Überwachung der Blickwinkel alle 10 Sekunden."""
    while True:
        
        if interrupt == True:
            break
        monitor_angles(left_angle, right_angle)
        
        focus_check()
        time.sleep(5)  # 10 Sekunden warten

def main():
    left_angle, right_angle = setup()

    if left_angle is not None and right_angle is not None:
        print(f"Linker Winkel: {left_angle} Grad")
        print(f"Rechter Winkel: {right_angle} Grad")
        print("Überwachung der Blickwinkel beginnt...")
        monitor(left_angle, right_angle)
    else:
        print("Setup fehlgeschlagen. Bitte erneut versuchen.")

if __name__ == "__main__":
    main()
