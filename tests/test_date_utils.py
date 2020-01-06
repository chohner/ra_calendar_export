import pytest
import datetime
import pytz
from ra_calendar_export import date_utils


def test_timestamp():
    assert (
        date_utils.timestamp(datetime.datetime(2020, 1, 1, 10, 30))
        == "2020-01-01_10-30-00"
    )


def test_date_from_dbY_str():
    assert date_utils.date_from_dbY_str(None) == None
    assert date_utils.date_from_dbY_str("17 Oct 2019") == datetime.date(2019, 10, 17)


@pytest.mark.parametrize(
    "test_input", ["01:00", " 01:00 ", "1:00"],
)
def test_time_from_24hr_str(test_input):
    assert date_utils.time_from_24hr_str(test_input) == datetime.time(1, 0)


@pytest.mark.parametrize(
    "test_input", ["a 01:00", "01:0 ", "24:00", "01:60"],
)
def test_test_time_from_24hr_str_fail(test_input):
    with pytest.raises(ValueError):
        date_utils.time_from_24hr_str(test_input)


def test_times_from_timespan():
    assert date_utils.times_from_timespan("10:00 - 17:00") == (
        datetime.time(10, 0),
        datetime.time(17, 0),
    )
    assert date_utils.times_from_timespan("22:00 - 05:00") == (
        datetime.time(22, 0),
        datetime.time(5, 0),
    )


def test_datetimes_from_dates_times_city():
    tz = pytz.timezone("Europe/Berlin")
    event_start_dt, event_end_dt = date_utils.datetimes_from_dates_times_city(
        datetime.date(2019, 12, 10), datetime.time(10, 0), datetime.time(17, 0)
    )
    assert event_start_dt == datetime.datetime(2019, 12, 10, 10, 0, tzinfo=tz)
    assert event_end_dt == datetime.datetime(2019, 12, 10, 17, 0, tzinfo=tz)

    # time_end < time_start, no date_end
    event_start_dt, event_end_dt = date_utils.datetimes_from_dates_times_city(
        datetime.date(2019, 12, 10), datetime.time(10, 0), datetime.time(5, 0),
    )
    assert event_start_dt == datetime.datetime(2019, 12, 10, 10, 0, tzinfo=tz)
    assert event_end_dt == datetime.datetime(2019, 12, 11, 5, 0, tzinfo=tz)

    # time_end < time_start, with date_end
    event_start_dt, event_end_dt = date_utils.datetimes_from_dates_times_city(
        datetime.date(2019, 12, 10),
        datetime.time(10, 0),
        datetime.time(5, 0),
        datetime.date(2019, 12, 15),
    )
    assert event_start_dt == datetime.datetime(2019, 12, 10, 10, 0, tzinfo=tz)
    assert event_end_dt == datetime.datetime(2019, 12, 15, 5, 0, tzinfo=tz)

    event_start_dt, event_end_dt = date_utils.datetimes_from_dates_times_city(
        datetime.date(2019, 12, 10),
        datetime.time(10, 0),
        datetime.time(19, 0),
        city="boston",
    )
    tz_boston = pytz.timezone("America/New_York")
    assert event_start_dt == datetime.datetime(2019, 12, 10, 10, 0, tzinfo=tz_boston)
    assert event_end_dt == datetime.datetime(2019, 12, 10, 19, 0, tzinfo=tz_boston)


def test_timezone_from_city():
    assert date_utils.timezone_from_city("berlin") == pytz.timezone("Europe/Berlin")
    assert date_utils.timezone_from_city(" berlin ") == pytz.timezone("Europe/Berlin")
    assert date_utils.timezone_from_city("boston") == pytz.timezone("America/New_York")
