import time
import pytz
import requests
import pandas as pd
from datetime import datetime
from io import StringIO
from .exceptions import DelistedCode

headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Cache-Control': 'no-cache, max-age=0'
    }

class KabutanScraper(object):
    """Scraper for Kabutan(株探)
    """

    def __init__(self, code: str):
        self.code = code.upper().replace('.T', '')

    def get_stock_price_by_minutes(self) -> pd.DataFrame:
        """Get stock price data by minute.

        Returns:
            pd.DataFrame: A DataFrame containing stock prices indexed by minute.

        Raises:
            DelistedCode: If the stock code has been delisted.

        Example:
            >>> from some_module import KabutanScraper
            >>> kt = KabutanScraper('7203.T')
            >>> df = kt.get_stock_price_by_minutes()
        """
        url = "https://kabutan.jp/stock/read?c={}&m=4&k=1&{}=".format(self.code, int(time.time() * 1000))
        response = requests.get(url=url, headers=headers)
        html = response.text

        if len(html) < 10:
            raise DelistedCode(code=self.code) 
        
        csvStringIO = StringIO(html)
        df = pd.read_csv(csvStringIO, sep=",", header=None)
        
        df = df.iloc[1:]    # Drop the first row, dummy data

        def convert_to_datetime(date1, date2):
            # Combine the two dates
            combined_date = date2 + date1[-6:]

            # Convert to datetime object
            datetime_obj = datetime.strptime(combined_date, "%Y.%m.%d/%H:%M")

            # Define the timezone for Asia/Tokyo
            tokyo_tz = pytz.timezone('Asia/Tokyo')

            # Localize the naive datetime object to the Tokyo timezone
            datetime_obj_with_tz = tokyo_tz.localize(datetime_obj)

            return datetime_obj_with_tz

        df['date'] = df.apply(lambda x: convert_to_datetime(x[0], x[6]), axis=1)
        df = df.rename(columns={1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'}, inplace=False)
        df = df.drop([0, 6,7,8,9,10,11], axis=1)   # Drop unneeded columns

        # Multiply 0.1 & typecasting(for decimal point is not displayed).
        for col in ['open', 'high', 'low', 'close']:
            df[col] = df[col].astype('int')
            df[[col]] = df[[col]].apply(lambda x: (x * 0.1).astype(float))

        df = df.sort_values(by=['date'])
        df = df.set_index('date')
        
        return df