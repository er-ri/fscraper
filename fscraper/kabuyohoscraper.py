import time
import json
import requests
import email.utils
import pandas as pd


class KabuyohoScraper(object):

    def __init__(self, bcode):
        self.__bcode = bcode.replace('.T', '')

    def get_target_price(self) -> pd.DataFrame:
        """Get theory PB/R and PE/R market price from sbisec API.("https://img-sec.ifis.co.jp")

        Returns: 
            Dataframe including target price

        """
        # `Request` without `Referer`` paramter will be blocked by the website.
        scraper_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Referer': 'https://kabuyoho.jp/'
        }

        # Put the url here while a timestamp is necessary.
        target_price_api = "https://img-sec.ifis.co.jp/graph/stock_chart_tp/{}.json?callback=tp{}&_={}".format(
            self.__bcode, self.__bcode, int(time.time() * 1000))

        # Convert the response to json Object.
        resp = requests.get(url=target_price_api, headers=scraper_headers)
        record_date = email.utils.parsedate_to_datetime(
            resp.headers['Last-Modified']).strftime("%Y-%m-%d")
        html = resp.text
        resp_raw = html.split("(", 1)[1].strip(")")
        resp_json = json.loads(resp_raw)

        # Extract the necessary data.
        pbr_low = resp_json[0]['data'][0]['low']
        pbr_high = resp_json[0]['data'][0]['high']
        pbr_theory = resp_json[3]['data'][0]['y']
        per_low = resp_json[1]['data'][0]['low']
        per_high = resp_json[1]['data'][0]['high']
        per_theory = resp_json[5]['data'][0]['y']
        current_price = resp_json[2]['data'][0]['y']
        target_price = resp_json[7]['data'][0]['y']

        # Construct dataframe
        df = pd.DataFrame(index=range(1))
        df.insert(len(df.columns), 'code', self.__bcode + '.T')
        df.insert(len(df.columns), 'record_date', record_date)
        df.insert(len(df.columns), 'current_price', current_price)
        df.insert(len(df.columns), 'pbr_low', pbr_low)
        df.insert(len(df.columns), 'pbr_high', pbr_high)
        df.insert(len(df.columns), 'pbr_theory', pbr_theory)
        df.insert(len(df.columns), 'per_low', per_low)
        df.insert(len(df.columns), 'per_high', per_high)
        df.insert(len(df.columns), 'per_theory', per_theory)
        df.insert(len(df.columns), 'target_price', target_price)

        return df
