

Go to:



# Education Bot

Der **Education Bot** ist ein interaktives Lehrassistenzsystem, das speziell für Modul interaktive Benutzerschnittstellen der Hochschule Karlsruhe gebaut wurde. Der Bot kombiniert Sprachverarbeitung, Gesichtsanzeigen und State-Machine-Steuerung, um ein dynamisches und personalisiertes Lernerlebnis zu bieten. Das System ermöglicht freie Lernmodi, Fragerunden sowie Aufmerksamkeitserkennung, um den Lernprozess zu optimieren.

## Inhaltsverzeichnis
1. [Übersicht der Subsysteme](#übersicht-der-subsysteme)
   - [State Machine](#state-machine)
   - [Audio Recorder](#audio-recorder)
   - [Command Validator](#command-validator)
   - [Robot Face](#robot-face)
   - [LLM Query](#llm-query)
   - [Head Pose Estimation](#head-pose-estimation)

2. [Nutzung](#nutzung)


---

## Übersicht der Subsysteme

### 1. State Machine
- **Pfad**: `StateMaschine/state_machine.py`
- **Beschreibung**: Die State Machine steuert den gesamten Ablauf des Bots und verwaltet die verschiedenen Zustände:
  - `init`: Initialer Zustand.
  - `startedBot`: Der Bot ist aktiv und bereit.
  - `free_learning`: Freier Lernmodus.
  - `Q_and_A`: Fragerundenmodus.
  - `completed`: Der Bot beendet seine Aufgabe.
- **Wichtigste Methoden**:
  - `start_bot()`: Übergang von `init` zu `startedBot`.
  - `start_free_learning()`: Aktiviert den freien Lernmodus.
  - `transition_to_completed()`: Beendet den aktuellen Zustand.

### 2. Audio Recorder
- **Pfad**: `TTS_and_STT/AudioRecorder.py`
- **Beschreibung**: Verarbeitet Sprachaufnahmen des Nutzers und wandelt sie mithilfe von Whisper in Text um.
- **Funktionen**:
  - `start_audio_input()`: Startet die Aufnahme.
  - `transcribe_with_whisper()`: Transkribiert die aufgezeichnete Audiodatei in Text.

### 3. Command Validator
- **Pfad**: `Commands/CommandValidator.py`
- **Beschreibung**: Der Command Validator überprüft und validiert Nutzerbefehle. Diese werden mithilfe von Fuzzy-Matching den vorgesehenen Aktionen zugeordnet.
- **Funktionen**:
  - `validate_and_process(command)`: Verarbeitet einen Befehl und leitet die entsprechende Aktion ein.
- **Unterstützte Befehle**:
  - `start`, `free learning`, `fragerunde`, `end bot`.

### 4. Robot Face
- **Pfad**: `Face_Display/pylips`
- **Beschreibung**: Dieses Subsystem steuert die visuelle Repräsentation des Bots über Gesichtsausdrücke und Sprachausgabe.
- **Funktionen**:
  - `set_appearance(preset)`: Ändert das Gesicht des Bots (z. B. Schlafmodus).
  - `express(expression, duration)`: Zeigt Emotionen basierend auf dem aktuellen Zustand.
  - `say(text)`: Gibt Text als Sprachausgabe aus.

### 5. LLM Query
- **Pfad**: `LLM/llm_query.py`
- **Beschreibung**: Das Subsystem nutzt ein Language Model (Mistral), um Fragen des Nutzers zu beantworten und Kontextinformationen bereitzustellen.
- **Funktionen**:
  - `query_Q_AND_A(context, question, slide_path, output_path)`: Stellt eine Frage an das Modell und verarbeitet die Antwort.

### 6. Head Pose Estimation
- **Pfad**: `HeadPoseEstimation/distractionDetection.py`
- **Beschreibung**: Überwacht die Aufmerksamkeit des Nutzers, indem es die Kopfhaltung analysiert. Das System nutzt YOLO, um die Kopfposition zu tracken und Ablenkungen zu erkennen.
- **Funktionen**:
  - `setup()`: Initiale Kalibrierung des Kopfes.
  - `monitor_angles(left_angle, right_angle)`: Überwacht die Kopfhaltung und meldet Ablenkungen.

---

## Installation
1. Klone das Repository:
   ```bash
   git clone https://github.com/CaVincenzo/education_bot.git
   ```
2. Installiere die Abhängigkeiten:

## Nutzung
1. Starte den Server des Bots:
   ```bash
        python -m pylips.face.start
   ```
   Go to, http://localhost:8000/face
2. Starte die main.py im Rootverzeichnis. 
3. Interagiere mit dem Bot über Sprachbefehle:
   - `Start`: Aktiviert den Bot.
   - `Freies Lernen`: Wechselt in den freien Lernmodus.
   - `Fragerunde`: Beginnt eine Frage-Antwort-Session.
   - `Beenden`: Beendet den Bot.
3. Der Bot reagiert visuell und sprachlich auf Eingaben und überwacht den Nutzer während der Sitzung.

---

## Zukünftige Verbesserungen


---