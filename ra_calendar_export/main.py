import datetime
import ics
from .networking import event_ids_from_profile
from .parse import event
from .date_utils import timestamp


def ics_file_from_profile(username, password=None, filename=None):
    """Saves events to ics file for a given username. Password needed for private profiles."""
    ics_events = events_from_profile(username, password, as_ics=True)
    ics_calendar = ics.Calendar(events=ics_events)
    filename = filename if filename else f"{username}_{timestamp()}.ics"
    with open(filename, "w") as file:
        file.writelines(ics_calendar)


def events_from_ids(eventid_list, as_ics=False):
    """Create events given a list of event ids"""
    if type(eventid_list) not in [tuple, list]:
        eventid_list = [eventid_list]
    event_list = [event.Event(from_id=event_id) for event_id in eventid_list]
    return [e.as_ics() for e in event_list] if as_ics else event_list


def events_from_profile(username, password=None, as_ics=False):
    """Get events for given username. Password needed for private profiles."""
    event_ids = event_ids_from_profile(username, password)
    return events_from_ids(event_ids, as_ics)
