from bs4 import BeautifulSoup
import ics
from .. import networking
from ..date_utils import (
    date_from_dbY_str,
    datetimes_from_dates_times_city,
    times_from_timespan,
)


class Event:
    def __init__(
        self, from_id=None, from_html=None, from_dict=None,
    ):
        if not from_id and not from_html and not from_dict:
            raise ValueError("Event must be initialized with either id, html, or dict")
        if from_id:
            self._get_from_id(from_id)
        elif from_html:
            self._get_from_html(from_html)
        else:
            self._from_dict(from_dict)

    def _get_from_id(self, event_id):
        """Fetch event information from RA based on event id"""
        event_html = networking.get_event_from_id(event_id)
        self._get_from_html(event_html)

    def _get_from_html(self, event_html):
        """Parse event html"""
        event_soup = soup_from_html(event_html)
        event_details = details_from_soup(event_soup)
        self.name = name_from_soup(event_soup)
        self.url = url_from_soup(event_soup)
        self.begin, self.end = datetimes_from_details(event_details)
        self.location = location_from_details(event_details)
        self.description = description_from_soup(event_soup)

    def _from_dict(self, event_dict):
        """Init event using a dict of name, begin, end, location, description (all optional)"""
        try:
            self.name = event_dict["name"]
            self.begin = event_dict["begin"]
            self.end = event_dict["end"]
            self.url = event_dict["url"]
            self.location = event_dict["location"]
            self.description = event_dict["description"]
        except KeyError:
            pass

    def as_ics(self):
        return ics.Event(
            url=self.url,
            begin=self.begin,
            end=self.end,
            name=self.name,
            location=self.location,
            description=self.description,
        )

    def __repr__(self):
        return f"{self.name} ({self.url})\n{self.begin} to {self.end}\n{self.location}"


def soup_from_html(event_html):
    return BeautifulSoup(event_html, "html.parser")


def url_from_soup(event_soup):
    return event_soup.find("meta", attrs={"property": "og:url"})["content"]


def name_from_soup(event_soup):
    return event_soup.find("meta", attrs={"property": "og:title"})["content"]


def description_from_soup(event_soup):
    description = (
        event_soup.find("div", {"class": "left"}).find_all("p")[1].text.strip()
    )
    lineup_html = event_soup.find("p", {"class": "lineup"}).find_all("a")
    lineup_list = "".join([f"- {artist.text.strip()}\n" for artist in lineup_html])
    return f"{lineup_list}\n{description}"


def details_from_soup(event_soup):
    return event_soup.find("aside", {"id": "detail"})


def dates_from_details(event_details):
    date_links = event_details.li.find_all("a")
    start_date_str = date_links[0].text.strip()
    end_date_str = date_links[1].text.strip() if len(date_links) > 1 else None
    return date_from_dbY_str(start_date_str), date_from_dbY_str(end_date_str)


def location_from_details(event_details):
    venue_details = event_details.find_all("li")[1]
    venue_name = venue_details.a.text
    venue_adress = venue_details.contents[3].strip()
    return f"{venue_name}\n{venue_adress}"


def datetimes_from_details(event_details):
    time_span = event_details.li.find_all("a")[-1].next_sibling.next_sibling
    event_day_start, event_day_end = dates_from_details(event_details)
    city = event_details.a.attrs["href"].split("/")[3]
    return datetimes_from_dates_times_city(
        event_day_start, *times_from_timespan(time_span), event_day_end, city
    )
