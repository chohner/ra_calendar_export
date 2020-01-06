import pickle
import datetime
from pathlib import Path
import bs4
import pytz
from ra_calendar_export.parse import event
import pytest

TEST_DATA_PATH = Path(__file__).parent / "test_data"

with open(TEST_DATA_PATH / "event_single_day.pkl", "rb") as f:
    single_day_resp = pickle.load(f)

with open(TEST_DATA_PATH / "event_multi_day.pkl", "rb") as f:
    multi_day_resp = pickle.load(f)


def test_soup_from_html():
    event_soup = event.soup_from_html(single_day_resp.text)
    assert type(event_soup) is bs4.BeautifulSoup
    assert ~event_soup.is_empty_element


def test_url_from_soup():
    url = event.url_from_soup(event.soup_from_html(single_day_resp.text))
    assert url == "https://www.residentadvisor.net/events/1360531"


def test_name_from_soup():
    name = event.name_from_soup(event.soup_from_html(single_day_resp.text))
    assert name == "Expeditions N017"


def test_description_from_soup():
    description = event.description_from_soup(
        event.soup_from_html(single_day_resp.text)
    )
    expected_description = (
        "- Black Lotus\n"
        "- Mary Velo\n"
        "- lego\n"
        "- Zusan\n"
        "\n"
        "thank you dear <3 \n"
        "\n"
        "here's another quick one:\n"
        "\n"
        "After entering its third year, our journey sets its course towards the sun. At the beginning of March it might be too presumptuous to seek warmth, however, the days are longer, the streets are brighter, and just a quick glimpse at our sailors will reveal the encouraging sight of careful optimism. \n"
        'Despite the above said, this edition of our Expeditions might be darker than usual. Normally, the first half of our journey is lighter, more forgiving. This time, we\'re afraid that at least three thirds of our ship captains do not know the meaning of the term "light", when it comes to Techno. We know, it is the end of the winter and you need all the energy you can get in order to make that last step, before the first rays of sun can caress your faces. This, in so many words, is the concept behind this specific Expedition: to remind you that it is always the darkest before sunrise. \n'
        "Remember: when it gets too obscure and too demanding, we shall wait for with the compete contrast in the garden tent. All you need to do is step out there, to the cold, for a brief moment, and let cosiness guide your way."
    )
    assert description == expected_description


def test_details_from_soup():
    event_soup = event.soup_from_html(single_day_resp.text)
    event_details = event.details_from_soup(event_soup)
    assert type(event_details) is bs4.element.Tag
    assert ~event_details.is_empty_element


def test_dates_from_details_single():
    event_details = event.details_from_soup(event.soup_from_html(single_day_resp.text))
    dates = event.dates_from_details(event_details)
    assert dates == (datetime.date(2020, 3, 5), None)


def test_dates_from_details_multi():
    event_details = event.details_from_soup(event.soup_from_html(multi_day_resp.text))
    dates = event.dates_from_details(event_details)
    assert dates == (datetime.date(2019, 12, 31), datetime.date(2020, 1, 2))


def test_location_from_details():
    event_details = event.details_from_soup(event.soup_from_html(multi_day_resp.text))
    location = event.location_from_details(event_details)
    assert location == "Griessmuehle\nSonnenallee 221; Neukölln; 12059 Berlin; Germany"


def test_datetimes_from_details_single():
    tz = pytz.timezone("Europe/Berlin")
    event_details = event.details_from_soup(event.soup_from_html(single_day_resp.text))
    datetime_start, datetime_end = event.datetimes_from_details(event_details)
    assert datetime_start == datetime.datetime(2020, 3, 5, 23, 59, tzinfo=tz)
    assert datetime_end == datetime.datetime(2020, 3, 6, 8, 0, tzinfo=tz)


def test_datetimes_from_details_multi():
    tz = pytz.timezone("Europe/Berlin")

    event_details = event.details_from_soup(event.soup_from_html(multi_day_resp.text))
    datetime_start, datetime_end = event.datetimes_from_details(event_details)
    assert datetime_start == datetime.datetime(2019, 12, 31, 22, 0, tzinfo=tz)
    assert datetime_end == datetime.datetime(2020, 1, 2, 10, 0, tzinfo=tz)


def test_Event_from_html_single():
    single_day_event = event.Event(from_html=single_day_resp.text)
    tz = pytz.timezone("Europe/Berlin")
    expected = {
        "url": "https://www.residentadvisor.net/events/1360531",
        "begin": datetime.datetime(2020, 3, 5, 23, 59, tzinfo=tz),
        "end": datetime.datetime(2020, 3, 6, 8, 0, tzinfo=tz),
        "name": "Expeditions N017",
        "location": "://about blank\nMarkgrafendamm 24c; Friedrichshain; 10245 Berlin; Germany",
    }

    for key in expected:
        assert single_day_event.__getattribute__(key) == expected[key]


def test_Event_from_html_multi():
    multi_day_event = event.Event(from_html=multi_day_resp.text)
    tz = pytz.timezone("Europe/Berlin")
    expected = {
        "url": "https://www.residentadvisor.net/events/1350471",
        "begin": datetime.datetime(2019, 12, 31, 22, 0, tzinfo=tz),
        "end": datetime.datetime(2020, 1, 2, 10, 0, tzinfo=tz),
        "name": "Zweitausendzwanzig",
        "location": "Griessmuehle\nSonnenallee 221; Neukölln; 12059 Berlin; Germany",
    }  # not checking description here

    for key in expected:
        assert multi_day_event.__getattribute__(key) == expected[key]


def test_Event_needs_init():
    with pytest.raises(ValueError):
        event.Event()


def test_Event_from_dict():
    tz = pytz.timezone("Europe/Berlin")
    expected = {
        "url": "https://www.residentadvisor.net/events/1360531",
        "begin": datetime.datetime(2020, 3, 5, 23, 59, tzinfo=tz),
        "end": datetime.datetime(2020, 3, 6, 8, 0, tzinfo=tz),
        "name": "Expeditions N017",
        "location": "://about blank\nMarkgrafendamm 24c; Friedrichshain; 10245 Berlin; Germany",
    }
    dict_event = event.Event(from_dict=expected)

    for key in expected:
        assert dict_event.__getattribute__(key) == expected[key]
