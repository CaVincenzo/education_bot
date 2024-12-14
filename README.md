# education Bot

## Structur
```mermaid
erDiagram
	main
	Spracheingabe
	Sprachausgabe
	Motoren
	AufmerkasmkeitSys
```


## State Machine
```mermaid
stateDiagram
	[*] --> Welcome
	Welcome --> Standard
	Standard --> Requests
	Requests --> Processing
	Processing --> Response
	Response --> Activation
	Standard --> Activation
	Activation --> [*]
	(Q&A)
	
	note left of Standard: happy face
	note left of Welcome: wave, happy face
	note left of Activation: wave, sad face
	note left of Requests: generate Voice Request
	note left of Processing: STT, LLM Request
	note left of Response: TTS
```


## Activity Diagram
```mermaid
flowchart TD
    A[Start: Initialisierung] --> B{Free Learning?}
    B -->|Yes| C[Free Learning]
    C --> D{Activation?}
    D -->|Yes| F[Activation]
    D -->|No| C
    B -->|No| H[Q&A Mode]
    H --> I{Done Learning?}
    C --> I
    I -->|Yes| J[Quit]
    I -->|No| H
    J --> K[Shutdown Everything]
    K --> L[End]

```


## State Diagram
```mermaid
stateDiagram
    [*] --> Initialisierung
    Initialisierung --> FreeLearning: Free Learning Mode selected
    FreeLearning --> Activation: Requires Activation
    Initialisierung --> QA: Q&A Mode selected
    QA --> Quit: Finish Learning
    FreeLearning --> Quit: Finish Learning
    Quit --> Shutdown
    Shutdown --> [*]

```


## ER-Modell
```mermaid
erDiagram
    Bot ||--o{ State : "Operates in"
    Bot ||--o{ Functionality : "Supports"
    Bot ||--o{ Sensor : "Equipped with"
    Bot ||--o{ Display : "Uses for interaction"
    User ||--o{ Bot : "Interacts with"

    State {
        string name
        string description
        string emotion
    }
    Functionality {
        string name
        string description
    }
    Sensor {
        string type
        string purpose
    }
    Display {
        string type
        string size
    }
    User {
        int id
        string name
    }
