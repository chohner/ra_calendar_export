import pickle
from ra_calendar_export.parse import token
from pathlib import Path

TEST_DATA_PATH = Path(__file__).parent / "test_data"


def test_parse_login_html():
    with open(TEST_DATA_PATH / "login_resp.pkl", "rb") as f:
        login_response = pickle.load(f)

    expected_token = "HsSV1GxUSXDldhho6AewhaFd7SJ9jlBCJhhcQ2PtnjQHgXFjwQLLrYxm9yydmPNl11QZ3ZwnrhRtG5527YzZ-xmCnes1"

    assert token.parse_login_html(login_response.text) == expected_token


def test_parse_login_html_empty():
    assert token.parse_login_html("<html></html>") is None
