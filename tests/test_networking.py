import pickle
from ra_calendar_export import networking


def test_build_payload():
    expected_payload = {
        "UsernameOrEmailAddress": "test_user",
        "Password": "test_pw",
        "__RequestVerificationToken": "auth_token",
    }
    payload = networking.build_payload("test_user", "test_pw", "auth_token")
    assert payload == expected_payload


def test_url_from_id():
    assert networking.url_from_id(1243) == "https://www.residentadvisor.net/events/1243"
