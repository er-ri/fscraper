class CodeNotFound(Exception):
    """YahooFinanceScraper: Raised when the code was not listed"""

    def __init__(self, code, message):
        self.code = code
        self.message = message


class InvalidFinancialReport(Exception):
    """YahooFinanceScraper: Raised when the requested report is invalid"""

    def __init__(self, report):
        self.message = f"Valid reports are 'incomestatement', 'balancesheet' and 'cashflow', but {report} received."


class InvalidFinancialReportType(Exception):
    """YahooFinanceScraper: Raised when the requested report type is invalid"""

    def __init__(self, report_type):
        self.message = f"Valid report types are 'quarterly' and 'annual', but {report_type} received."

