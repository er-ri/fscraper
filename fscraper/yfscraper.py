import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from .constant_table import (   
    REPORT_TABLE
)
from .exceptions import (
    CodeNotFound,
    InvalidFinancialReport,
    InvalidFinancialReportType
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Cache-Control': 'no-cache, max-age=0'
}


class YahooFinanceScraper(object):

    def __init__(self, code):
        self.code = code.upper()
        self._session = requests.Session()
        self._statistics_dom = None


    def get_financials(self, report, report_type):
        """Scrape Yahoo!Finance financial report

        Args:
            report(str): 'incomestatement' | 'balancesheet' | 'cashflow'
            quarterly(): 'quarterly' | 'annual'

        Returns:
            pd.DataFrame: corresponding report
        """
        # Accepted arguments check
        if report not in REPORT_TABLE.keys():
            raise InvalidFinancialReport(report=report)
        if report_type not in ['quarterly', 'annual']:
            raise InvalidFinancialReportType(type=report_type)

        items = REPORT_TABLE[report]
        items = [report_type + item for item in items]

        params = {
            'lang': 'en-US',
            'region': 'US',
            'symbol': f'{self.code}',
            'padTimeSeries': 'true',
            'type': ','.join(items),
            'merge': 'false',
            'period1': '493590046',
            'period2': f"{int(datetime.now().timestamp())}",
            'corsDomain': 'finance.yahoo.com',
        }

        response = self._session.get(
            f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self.code}',
            params=params,
            headers=headers,
        )
        raw = response.json()

        df = pd.DataFrame(columns=items)

        date_list = raw['timeseries']['result'][0]['timestamp']
        date_list = [datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d") for date in date_list]
        df['date']=date_list
        
        for _, item in enumerate(items):
            result = raw['timeseries']['result']
            records = next((raw[item] for raw in result if item in raw), None)
            values = [record['reportedValue']['raw'] if record is not None else '-'  for record in records]

            df[item]=values
        
        df = df.set_index('date').transpose()
        return df

    def get_stock_price(self, period='1mo', interval='1d'):
        """Get historical price 

        Args:
            period(str): `1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max`
            interval(str): `1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo`

        Returns:
            pd.DataFrame: stock price
        """
        params = dict()
        params['range'] = period
        params['interval'] = interval
        params['events'] = 'div'

        df = YahooFinanceScraper.__construct_price_dataframe(self, params)

        return df

    def get_stock_price2(self, start='', end = datetime.now().strftime('%Y-%m-%d'), interval='1d'):
        """Get history price with the specified date. 

        Args:
            start(str): start date, format `yyyy-mm-dd`
            end(str): end date, format `yyyy-mm-dd`
            interval(str): `1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo`

        Returns:
            pd.DataFrame: stock price
        """
        params = dict()
        params['period1'] = int(datetime.strptime(
            start, "%Y-%m-%d").timestamp())
        params['period2'] = int(datetime.strptime(end, "%Y-%m-%d").timestamp())
        params['interval'] = interval
        params['events'] = 'div'

        df = YahooFinanceScraper.__construct_price_dataframe(self, params)
        
        return df

    def __construct_price_dataframe(self, params):
        df = pd.DataFrame()

        url = "https://query2.finance.yahoo.com/v8/finance/chart/{}".format(
            self.code)
        html = self._session.get(url=url, params=params,
                            headers=headers).text
        price_json = json.loads(html)

        if price_json['chart']['error'] is not None:
            raise CodeNotFound(self.code, json.loads(html)[
                                        'chart']['error']['description'])

        df['date'] = price_json['chart']['result'][0]['timestamp']
        df['open'] = price_json['chart']['result'][0]['indicators']['quote'][0]['open']
        df['high'] = price_json['chart']['result'][0]['indicators']['quote'][0]['high']
        df['low'] = price_json['chart']['result'][0]['indicators']['quote'][0]['low']
        df['close'] = price_json['chart']['result'][0]['indicators']['quote'][0]['close']
        # Bugs: At specific times, inappropriated values of 'volume' are returned.
        df['volume'] = price_json['chart']['result'][0]['indicators']['quote'][0]['volume']

        # Add dividends if exists.
        try:
            for _, item in price_json['chart']['result'][0]['events']['dividends'].items():
                df.loc[df['date'] == item['date'],
                       'dividends'] = item['amount']
        except KeyError:
            df['dividends'] = np.nan

        df['date'] = df['date'].apply(lambda d: datetime.fromtimestamp(
            int(d)).strftime("%Y-%m-%d %H:%M:%S"))
        df = df.set_index('date')

        return df
