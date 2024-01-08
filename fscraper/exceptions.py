class CodeNotFoundException(Exception):
    """YahooFinanceScraper: Raised when the code was not listed"""

    def __init__(self, code, message):
        self.code = code
        self.message = message


class NoArticleFoundException(Exception):
    """ReutersScraper: Raised when no article was fetched for news scraper"""

    def __init__(self, message):
        self.message = message
