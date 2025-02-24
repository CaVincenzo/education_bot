import requests
import json
import urllib3
from pathlib import Path
from requests.exceptions import HTTPError
import aiohttp
import asyncio

# HTTPS-Warnungen deaktivieren
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MistralQuery:
    """
    Eine Klasse, die die Kommunikation mit dem Mistral LLM kapselt und Eingaben/Ausgaben verarbeitet.
    """
    def __init__(self):
        """
        Initialisiert die MistralQuery-Klasse mit einer URL zum LLM-Endpunkt.

        :param url: URL des LLM-Endpunkts.
        """
        self.url = "https://dellfi.serv.uni-hohenheim.de/mistral"

    def query_Q_AND_A(self, context, prompt, Foliensatz_file_path, output_file_path):
        """
        Kommuniziert mit dem Mistral LLM und verarbeitet Eingaben und Ausgaben unter Verwendung einer Eingabedatei.

        :param context: Vorbedingungen oder Kontext, der dem Prompt vorangestellt wird.
        :param prompt: Der Haupt-String, der vom Benutzer übergeben wird.
        :param input_file_path: Pfad zur Eingabedatei, die zusätzlichen Kontext enthält.
        :param output_file_path: Pfad zur Ausgabedatei, in die die Antwort geschrieben wird.
        :return: Die Antwort des LLM als String.
        """
        try:
            # Inhalte aus der Eingabedatei lesen
            try:
                context_content = Path(Foliensatz_file_path).read_text(encoding="utf-8")
            except FileNotFoundError:
                context_content = "Die benötigte Datei wurde nicht gefunden. Bitte stellen Sie sicher, dass die Eingabedatei vorhanden ist."

            # Vollständigen Kontext und Prompt kombinieren
            full_context = context + context_content
            full_prompt = full_context + "\n" + prompt

            # Anfrage an das LLM
            return  self._send_request(full_prompt, output_file_path)

        except Exception as err:
            return f"An error occurred in Q_AND_A: {err}"

        
    def query_FreeLearning(self, context, prompt, output_file_path):
        """
        Kommuniziert mit dem Mistral LLM und verarbeitet Eingaben und Ausgaben ohne Verwendung einer Eingabedatei.

        :param context: Vorbedingungen oder Kontext, der dem Prompt vorangestellt wird.
        :param prompt: Der Haupt-String, der vom Benutzer übergeben wird.
        :param output_file_path: Pfad zur Ausgabedatei, in die die Antwort geschrieben wird.
        :return: Die Antwort des LLM als String.
        """
        try:
            # Vollständigen Kontext und Prompt kombinieren
            full_prompt = context + "\n" + prompt

            # Anfrage an das LLM
            return self._send_request(full_prompt, output_file_path) 

        except Exception as err:
            return f"An error occurred in FL: {err}"
        



    def _send_request(self, full_prompt, output_file_path):
        """
        Führt die Anfrage an das LLM durch und speichert die Antwort.

        :param full_prompt: Der vollständige Prompt, der an das LLM gesendet wird.
        :param output_file_path: Pfad zur Ausgabedatei, in die die Antwort geschrieben wird.
        :return: Die Antwort des LLM als String.
        """
        try:
            data = {
                "model": "mistral-nemo",
                "prompt": full_prompt
            }
            response = requests.post(self.url, json=data, verify=False)
            
            # print(response._content.decode("utf-8"))
            
            if response.status_code == 200:
                lines = response.text.splitlines()
                full_response = "" # Variable für die Gesamtantwort des LLM
                
                for line in lines:
                    message = json.loads(line)
                    full_response += message["response"]
                    if message.get("done", False):
                        break

                # Antwort in die Ausgabedatei schreiben
                Path(output_file_path).write_text(full_response, encoding="utf-8")

                return  full_response
            else:
                return "Error: " + str(response.status_code)

        except HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except Exception as err:
            return f"An error occurred_send_request: {err}"


#  # Parameter definieren
#     context = "Du bist ein Lehrassistenz-System für Medieninformatiker aus dem 6. Semester.\n"
#     prompt = "Hallo bist du Online"
#     input_file_path = "LLM\Input.txt"
#     FL_output_file_path = "LLM\OutputFreeLearning.txt"
#     Q_and_A_output_file_path = "LLM\OutputQandA.txt"
#     # Rufe die Methode auf
#     
    
#     