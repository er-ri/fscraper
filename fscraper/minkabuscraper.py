import requests
import pandas as pd


class MinkabuScraper:
    """Minkabu Scraper from https://minkabu.jp/

    Attributes:
        code(str): ticker symbol
    """

    def __init__(self, code: str):
        self.code = code.replace('.T', '')

    def get_analysis(self):
        """Get Minkabu analysis data from https://minkabu.jp/stock/code/analysis

        Returns:
            pd.DataFrame: Analysis data including target price, theoretic_price and news, etc.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://minkabu.jp/',
            'ContentType': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://minkabu.jp',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }

        url = 'https://assets.minkabu.jp/jsons/stock-jam/stocks/{code}/lump.json'.format(
            code=self.code)

        raw_json = requests.get(url, headers=headers).json()

        df = pd.DataFrame()
        df['date'] = pd.to_datetime(raw_json['dates'])
        df['close'] = pd.to_numeric(raw_json['stock']['closes'])
        df['target_price'] = pd.to_numeric(raw_json['stock']['mk_prices'])
        df['predict_price'] = pd.to_numeric(raw_json['stock']['picks_prices'])
        df['theoretical_price'] = pd.to_numeric(
            raw_json['stock']['theoretic_prices'])
        df['volume'] = pd.to_numeric(raw_json['stock']['volumes'])

        df['news'] = raw_json['stock']['news']
        df['picks'] = raw_json['stock']['picks']
        df['n225'] = pd.to_numeric(raw_json['n225']['closes'])
        df['usdjpy'] = pd.to_numeric(raw_json['usdjpy']['closes'])

        df = df.set_index('date')
        return df
