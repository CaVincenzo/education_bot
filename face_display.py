import tkinter as tk
import logging

class FaceDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gesichtsanzeige")
        self.canvas = tk.Canvas(self.root, width=800, height=800, bg="white")
        self.canvas.pack()

        # Logging konfigurieren
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()]
        )

    def create_face(self, is_happy):
        # Canvas zurücksetzen
        self.canvas.delete("all")

        # Gesichtskreis
        self.canvas.create_oval(100, 100, 700, 700, fill="lightyellow", outline="black", width=2)

        # Augen
        self.canvas.create_rectangle(250, 300, 310, 360, fill="black")  # Linkes Auge
        self.canvas.create_rectangle(490, 300, 550, 360, fill="black")  # Rechtes Auge

        # Mund (lächelnd oder traurig)
        if is_happy:
            self.canvas.create_arc(250, 350, 550, 500, start=180, extent=180, style=tk.ARC, width=2)
        else:
            self.canvas.create_arc(250, 350, 550, 500, start=0, extent=180, style=tk.ARC, width=2)

        # Logge den Zustand von is_happy
        logging.info(f"IsFokus: {'isFokused and happy' if is_happy else 'notFokused and sad'}")

    def run(self):
        self.root.mainloop()

