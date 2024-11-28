
import requests
import json
import urllib3

from pathlib import Path # für Textfile

# HTTPS-Warnungen deaktivieren
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from requests.exceptions import HTTPError

# Funktion zur Kommunikation mit dem LLM
def query_mistral(prompt):
    url = "https://dellfi.serv.uni-hohenheim.de/mistral"
    data = {
        "model": "mistral-nemo",
        "prompt": prompt
    }
    response = requests.post(url, json=data, verify=False)

    if response.status_code == 200:
        lines = response.text.splitlines()
        full_response = ""
        for line in lines:
            message = json.loads(line)
            full_response += message["response"]
            if message.get("done", False):
                break
        return full_response
    else:
        return "Error: " + str(response.status_code)

# Hauptlogik 
def main():
    #print("Willkommen beim Voice Education Bot! Sprechen Sie, um zu starten.")

    while True: 

        # Input aus Textfile
        file_path = "/Users/valerieheil/Documents/Uni/HKA/Intuitive und perzeptive Benutzungsschnittstellen/Labor/3 Planung/"
        
        user_input = "Du bist ein Lehrassistenz-System für Medieninformatiker aus dem 6.Semester. Die folgenden Inhalte sollst du als Basis deiner Antwort nutzen, wenn du dies nicht kannst, dann halte dich bitte an eine allgemeine Antwort:"
        user_input = user_input + Path(file_path + "test.txt").read_text()
        # evtl als pdf bzw. pptx    

        # zum Testen in Terminal:
        user_input = user_input + input("Enter something: ")

        # Anfrage an das LLM
        bot_response = query_mistral(user_input)

        # als Text-File ausgeben, dann zu Speech weiterverarbeitet...
        Path(file_path + "text2").write_text(bot_response)
        print(user_input + " : ")
        print(bot_response)


if __name__ == "__main__":
    main()



# TODO
#
# State Machine mit Timer --> zu lange nichts passiert: promt: gebe eine Aktivierungs-Message aus (vllt auch letzten Inhalt nochmal zsmfassen)
# 
# aktuell noch kein Gedächtnis in LLM so, irgendwie mit ID? Session? --> irgendwas mitgeben, damit Prompt auf Folien eingeht
# wie ansprechen, dass LLM auf vorherige Inputs zugreifen kann bzw. auch auf Vorlesungsunterlagen
#  --> jedes Mal Infos mitschicken und gewünschte Folieninhalte










