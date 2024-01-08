import json
import requests
import pandas as pd
from .exceptions import NoArticleFoundException


class ReutersScraper(object):
    """
    JSON api interface('https://jp.reuters.com/companies/api/')
    """

    global __scraper_headers
    __scraper_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
    }

    def __init__(self, code):
        self.__code = code

        # Raw data(json), private member
        self.__raw_key_metrics = dict()
        self.__raw_financials = dict()
        self.__raw_event = dict()

    def __scrape_data(cls, url):
        try:
            resp = requests.get(url=url, headers=__scraper_headers).text
            data = json.loads(resp)
        except Exception as e:
            data = None
        return data

    def __extract_financial_statement(self, type, period):
        df = pd.DataFrame()
        raw_json = self.get_financials(
        )['market_data']['financial_statements'][type][period]

        for key in raw_json:
            df_ext = pd.DataFrame(raw_json[key])
            df_ext = df_ext.rename(columns={'value': key}).set_index('date')
            df = pd.concat([df, df_ext], axis=1)

        return df

    # Data retrieved from 'jp.reuters.com' API.
    def get_key_metrics(self):
        if bool(self.__raw_key_metrics) == False:
            url = 'https://jp.reuters.com/companies/api/getFetchCompanyKeyMetrics/{}'.format(
                self.__code)
            self.__raw_key_metrics = ReutersScraper.__scrape_data(url)
        return self.__raw_key_metrics

    def get_financials(self):
        if bool(self.__raw_financials) == False:
            url = 'https://jp.reuters.com/companies/api/getFetchCompanyFinancials/{}'.format(
                self.__code)
            self.__raw_financials = ReutersScraper.__scrape_data(url)
        return self.__raw_financials

    def get_event(self):
        if bool(self.__raw_event) == False:
            url = 'https://jp.reuters.com/companies/api/getFetchCompanyEvents/{}'.format(
                self.__code)
            self.__raw_event = ReutersScraper.__scrape_data(url)
        return self.__raw_event

    # Data factory
    def get_income_statement(self, period='annual'):
        """Retrieve income statement

        Args:
            period(str): 'annual' or 'interim' income statement

        Returns:
            pd.DataFrame: income statement
        """
        df = self.__extract_financial_statement('income', period)

        return df

    def get_balance_sheet(self, period='annual'):
        """Retrieve balance sheet

        Args:
            period(str): 'annual' or 'interim' blance sheet

        Returns:
            pd.DataFrame: balance sheet
        """
        df = self.__extract_financial_statement('balance_sheet', period)
        return df

    def get_cash_flow(self, period='annual'):
        """Get cash flow

        Args:
            period(str): 'annual' or 'interim' cash flow

        Returns:
            pd.DataFrame: cash flow
        """
        df = self.__extract_financial_statement('cash_flow', period)
        return df

    def get_news(self, keyword, size):
        params = {
            'query': f'{{"keyword":"{keyword}","offset":0,"orderby":"display_date:desc","size":{size},"website":"reuters-japan"}}',
            'd': '168',
            '_website': 'reuters-japan',
        }

        response = requests.get(
            'https://jp.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2',
            params=params,
            headers=__scraper_headers,
        )

        if response.json()['result']['pagination']['size'] < 1:
            raise NoArticleFoundException(
                f"No article was found with the keyword: {keyword}")

        return response.json()['result']['articles']
