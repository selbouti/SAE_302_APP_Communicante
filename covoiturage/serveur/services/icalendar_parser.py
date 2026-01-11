from icalendar import Calendar
from datetime import datetime


class ICalendarParser:
    """
    Utility class for parsing iCalendar (.ics) files.

    This class extracts calendar events and converts them
    into a list of trip-like dictionaries usable by the application.
    """

    @staticmethod
    def parse_events(ics_content):
        """
        Parse an iCalendar file content and extract events.

        Each event is converted into a dictionary containing
        basic information such as summary, description,
        start date/time, and location.

        :param ics_content: Raw content of the .ics file
        :type ics_content: bytes
        :return: List of parsed calendar events
        :rtype: list[dict]
        """
        trajets = []
        try:
            cal = Calendar.from_ical(ics_content)
            for component in cal.walk():
                if component.name == "VEVENT":
                    event = {
                        'summary': str(component.get('summary', '')),
                        'description': str(component.get('description', '')),
                        'dtstart': component.get('dtstart').dt
                        if component.get('dtstart') else None,
                        'location': str(component.get('location', ''))
                    }
                    trajets.append(event)
        except Exception as e:
            print(f"Erreur parsing iCalendar: {e}")
        return trajets
