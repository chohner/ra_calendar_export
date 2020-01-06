import datetime
import pytz
import re
from .timezone_lookup import TIMEZONE_LOOKUP


def timestamp(dt=None):
    """Datetime formated as 2020-01-21_20-25-57. Return current time if None is passed"""
    dt = dt if type(dt) is datetime.datetime else datetime.datetime.now()
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def timezone_from_city(city):
    """pytz.timezone for all cities listed on RA"""
    return pytz.timezone(TIMEZONE_LOOKUP[city.strip()])


def time_from_24hr_str(str_24hr):
    """Parse '10:00' into [10, 0]. Strips whitespace, returns None on fail"""
    match = re.match(r"^(?:\d|[01]\d|2[0-3]):[0-5]\d$", str_24hr.strip())
    try:
        time_as_int = [int(num) for num in match.group().split(":")]
    except AttributeError as e:
        raise ValueError("Input didn't parse as 24hr string") from e
    return datetime.time(*time_as_int)


def date_from_dbY_str(d_b_Y_str):
    """Parse 'd b Y' string (eg '17 Oct 2019') into datetime. Returns None on fail"""
    return (
        None
        if d_b_Y_str is None
        else datetime.datetime.strptime(d_b_Y_str, "%d %b %Y").date()
    )


def times_from_timespan(timespan_str):
    """Parse 10:00 - 17:00 to two datetime.time objects"""
    starttime_str, endtime_str = timespan_str.split("-")
    return time_from_24hr_str(starttime_str), time_from_24hr_str(endtime_str)


def datetimes_from_dates_times_city(
    date_start, time_start, time_end, date_end=None, city="berlin"
):
    """Datetimes for start & end of an event.

    date_end is optional (defaults to same day if time_end > time start, else next day).
    city is optional (defaults to 'berlin')
    """
    if date_end is None:
        date_end = (
            date_start
            if time_start < time_end
            else date_start + datetime.timedelta(days=1)
        )
    timezone = timezone_from_city(city)
    event_start_dt = datetime.datetime.combine(date_start, time_start, tzinfo=timezone)
    event_end_dt = datetime.datetime.combine(date_end, time_end, tzinfo=timezone)
    return event_start_dt, event_end_dt
