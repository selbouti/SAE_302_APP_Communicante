from icalendar import Calendar
from datetime import datetime, time
import requests


class EDTParser:

    # ------------------------------
    # Charger un fichier .ics local
    # ------------------------------
    def load_from_file(self, file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return Calendar.from_ical(data)

    # ------------------------------
    # Charger un fichier .ics via URL
    # ------------------------------
    def load_from_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return Calendar.from_ical(response.content)

    # ------------------------------
    # Extraire événements d’un jour
    # ------------------------------
    def extract_events_for_day(self, calendar_obj, date_cible):
        """
        Retourne une liste [(heure_debut, heure_fin)]
        """
        events = []

        for component in calendar_obj.walk():
            if component.name != "VEVENT":
                continue

            dtstart = component.get("DTSTART").dt
            dtend = component.get("DTEND").dt

            if isinstance(dtstart, datetime) and dtstart.date() == date_cible:
                events.append((dtstart.time(), dtend.time()))

        return events

    # ------------------------------
    # Calcul des disponibilités
    # ------------------------------
    def compute_disponibilites(self, events):
        """
        events : [(time_debut, time_fin)]
        Retourne les plages disponibles
        """
        JOUR_DEBUT = time(8, 0)
        JOUR_FIN = time(18, 0)

        events = sorted(events)
        dispos = []

        current = JOUR_DEBUT

        for start, end in events:
            if start > current:
                dispos.append((current, start))
            current = max(current, end)

        if current < JOUR_FIN:
            dispos.append((current, JOUR_FIN))

        return dispos
