import pickle
from pathlib import Path
from ra_calendar_export.parse import calendar

TEST_DATA_PATH = Path(__file__).parent / "test_data"


def test_parse_calendar_empty():
    assert calendar.parse_calendar_html("<html></html>") == ([], None)


def test_parse_calendar_html():
    with open(TEST_DATA_PATH / "calendar_resp.pkl", "rb") as f:
        cal_resp = pickle.load(f)

    expected_events = [1358858, 1352146]
    assert calendar.parse_calendar_html(cal_resp.text) == (
        expected_events,
        "calendar?mn=2&yr=2020",
    )


def test_parse_calendar_html_no_next():
    with open(TEST_DATA_PATH / "calendar_resp_no_next.pkl", "rb") as f:
        cal_resp = pickle.load(f)

    expected_events = [1358858, 1352146]
    assert calendar.parse_calendar_html(cal_resp.text) == (expected_events, None)
