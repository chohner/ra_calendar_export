import requests
from .parse import token, calendar

BASE_URL = "https://www.residentadvisor.net"
LOGIN_URL = f"{BASE_URL}/login"
EVENTS_URL = f"{BASE_URL}/events"


def url_from_id(event_id):
    return f"{EVENTS_URL}/{event_id}"


def get_event_from_id(event_id):
    event_resp = requests.get(url_from_id(event_id))
    assert event_resp.status_code == 200
    return event_resp.text


def get_auth_token(session):
    """Get auth token from 'https://www.residentadvisor.net/login' using the passed session"""
    login_response = session.get(LOGIN_URL)
    assert login_response.status_code == 200
    return token.parse_login_html(login_response.text)


def post_login(session, payload):
    """Post payload to login url using the given session. Returns login response"""
    return session.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))


def perform_login(session, username, password):
    """Build payload and perform login using given session. Returns login response"""
    auth_token = get_auth_token(session)
    login_payload = build_payload(username, password, auth_token)
    return post_login(session, login_payload)


def event_ids_from_profile(username, password=None):
    """Return list of event_ids based on username. Password is needed for private profiles"""
    profile_url = f"{BASE_URL}/profile/{username}"
    all_events = []

    with requests.Session() as session:
        if password is not None:
            login_response = perform_login(session, username, password)
            assert login_response.status_code == 200

        next_page = f"{profile_url}/calendar"

        while next_page is not None:
            print(f"requesting {next_page}")

            cal_response = session.get(next_page, headers=dict(referer=profile_url))
            assert cal_response.status_code == 200

            events, next_month_href = calendar.parse_calendar_html(cal_response.text)
            all_events += events
            next_page = (
                None if next_month_href is None else f"{profile_url}/{next_month_href}"
            )
    return all_events


def build_payload(username, password, auth_token):
    return {
        "UsernameOrEmailAddress": username,
        "Password": password,
        "__RequestVerificationToken": auth_token,
    }
