import cv2
from ultralytics import YOLO
from PIL import Image
import numpy as np
import math
import time

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

def setup():
    #Setup-Funktion zur Aufnahme der Links- und Rechts-Winkel.
    print("Bitte nach links schauen und Enter drücken.")
    input("Drücken Sie Enter, nachdem Sie bereit sind...")
    
    left_image_path = capture_image("left_view.png")
    if not left_image_path:
        print("Fehler beim Aufnehmen des linken Bildes.")
        return None, None
    left_angle = analyze_image_with_yolo(left_image_path)

    print("Bitte nach rechts schauen und Enter drücken.")
    input("Drücken Sie Enter, nachdem Sie bereit sind...")
    right_image_path = capture_image("right_view.png")
    if not right_image_path:
        print("Fehler beim Aufnehmen des rechten Bildes.")
        return None, None
    right_angle = analyze_image_with_yolo(right_image_path)

    return left_angle, right_angle

def monitor_angles(left_angle, right_angle):
    """Funktion zur Überwachung der Blickwinkel alle 10 Sekunden."""
    while True:
        print("Neues Bild wird aufgenommen...")
        current_image_path = capture_image("current_view.png")
        if not current_image_path:
            print("Fehler beim Aufnehmen des aktuellen Bildes.")
            continue
        current_angle = analyze_image_with_yolo(current_image_path)

        if current_angle < left_angle:
            print("Warnung: Person schaut weiter nach links als im Setup angegeben!")
        elif current_angle > right_angle:
            print("Warnung: Person schaut weiter nach rechts als im Setup angegeben!")
        else:
            print("Blickwinkel ist innerhalb des zulässigen Bereichs.")

        time.sleep(10)  # 10 Sekunden warten

def main():
    print("Setup: Wir werden die Winkel für links und rechts aufnehmen.")
    left_angle, right_angle = setup()

    if left_angle is not None and right_angle is not None:
        print(f"Linker Winkel: {left_angle} Grad")
        print(f"Rechter Winkel: {right_angle} Grad")
        print("Überwachung der Blickwinkel beginnt...")
        monitor_angles(left_angle, right_angle)
    else:
        print("Setup fehlgeschlagen. Bitte erneut versuchen.")

if __name__ == "__main__":
    main()
