from icalendar import Calendar
from datetime import datetime

class ICalendarParser:
    @staticmethod
    def parse_events(ics_content):
        """Parse fichier iCalendar et retourne liste des trajets"""
        trajets = []
        try:
            cal = Calendar.from_ical(ics_content)
            for component in cal.walk():
                if component.name == "VEVENT":
                    event = {
                        'summary': str(component.get('summary', '')),
                        'description': str(component.get('description', '')),
                        'dtstart': component.get('dtstart').dt if component.get('dtstart') else None,
                        'location': str(component.get('location', ''))
                    }
                    trajets.append(event)
        except Exception as e:
            print(f"Erreur parsing iCalendar: {e}")
        return trajets