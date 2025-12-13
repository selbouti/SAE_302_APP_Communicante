# services/edt_parser.py

from icalendar import Calendar
from datetime import datetime
import requests

class EDTParser:

    # ---------------------------------------------------
    # Charger un fichier .ics (local)
    # ---------------------------------------------------
    def load_from_file(self, file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return Calendar.from_ical(data)

    # ---------------------------------------------------
    # Charger un fichier .ics depuis une URL
    # ---------------------------------------------------
    def load_from_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return Calendar.from_ical(response.content)

    # ---------------------------------------------------
    # Extraire HOIRAIRES ALLER / RETOUR sur un jour donné
    # ---------------------------------------------------
    def extract_day_schedule(self, calendar_obj, date_cible):
        """
        date_cible = datetime.date()
        Retour :
        { "aller": datetime, "retour": datetime }
        """

        horaires = {"aller": None, "retour": None}

        for component in calendar_obj.walk():
            if component.name != "VEVENT":
                continue

            dtstart = component.get("DTSTART").dt
            dtend = component.get("DTEND").dt

            # On garde uniquement les événements du jour donné
            if dtstart.date() != date_cible:
                continue

            # Hypothèse : premier événement = ALLER, dernier = RETOUR
            if horaires["aller"] is None:
                horaires["aller"] = dtstart
            horaires["retour"] = dtend

        return horaires
