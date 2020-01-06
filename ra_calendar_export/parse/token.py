from html.parser import HTMLParser


class AuthTokenParser(HTMLParser):
    """Using html.parser.HTMLParser instead of BeautifulSoup for practise"""

    def __init__(self):
        """Init instance variables then call HTMLParser init"""
        self.auth_token = None
        super().__init__()

    def handle_starttag(self, tag, attrs):
        """Check whether attributes contain '__RequestVerificationToken'. If so, save adjacent auth_token"""
        for attr_name, attr_val in attrs:
            if attr_val == "__RequestVerificationToken":
                for attr_name, attr_val in attrs:
                    if attr_name == "value":
                        self.auth_token = attr_val


def parse_login_html(login_response_text):
    """"Parses auth_token from a login response object. Returns None if not found"""
    authtoken_parser = AuthTokenParser()
    authtoken_parser.feed(login_response_text)
    return authtoken_parser.auth_token
