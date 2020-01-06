from html.parser import HTMLParser


class CalendarParser(HTMLParser):
    """Parses events of single calender page into self.events and saves next_page is available"""

    def __init__(self):
        """Init instance variables then call HTMLParser init"""
        self.inside_td_hasEvents = False
        self.inside_liNext = False
        self.events = []
        self.next_page = None
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "td":  # Check whether inside has_events td
            for attr_name, attr_val in attrs:
                if attr_name == "class" and "hasEvents" in attr_val.split(" "):
                    self.inside_td_hasEvents = True
        elif tag == "li":  # check whether inside liNext
            for attr_name, attr_val in attrs:
                if attr_name == "id" and attr_val == "liNext":
                    self.inside_liNext = True
        elif (
            self.inside_td_hasEvents and tag == "a"
        ):  # If inside hasEvents: save event id
            for attr_name, attr_val in attrs:
                if attr_name == "href" and attr_val[7] == "/":
                    event_id = int(attr_val[8:])
                    if event_id not in self.events:
                        self.events.append(event_id)
        elif (
            self.inside_liNext and tag == "a"
        ):  # If inside liNext: save next_page if it exists
            for attr_name, attr_val in attrs:
                if attr_name == "href":
                    self.next_page = attr_val

    def handle_endtag(self, tag):
        if self.inside_td_hasEvents and tag == "td":
            self.inside_td_hasEvents = False
        elif self.inside_liNext and tag == "li":
            self.inside_liNext = False


def parse_calendar_html(cal_response_text):
    calendar_parser = CalendarParser()
    calendar_parser.feed(cal_response_text)
    return calendar_parser.events, calendar_parser.next_page


# def cal_soup_to_ics_events(cal_soup):
#     days_with_events = cal_soup.find_all("td", {"class": "hasEvents"})
#     ics_events = []
#     for day_with_event in days_with_events:
#         for event_on_day in day_with_event.find_all("div", {"class": "pb2"}):
#             event_url = base_url + event_on_day.a.get("href")
#             event_response = session.get(event_url, headers=dict(referer=cal_url))
#             event_soup = BeautifulSoup(event_response.text, "html.parser")
#             ics_events.append(ics_event_from_event_soup(event_soup, event_url))
#     return ics_events
