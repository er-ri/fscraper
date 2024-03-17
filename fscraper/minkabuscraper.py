import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
}


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

        url = f"https://assets.minkabu.jp/jsons/stock-jam/stocks/{self.code}/lump.json"

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

    def get_news_abstract(self):
        """Get the news abstract from minkabu

        Returns:
            list: news abstract
        """
        url = f"https://minkabu.jp/stock/{self.code}/news"

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, "html.parser")
        cells = soup.select("div[class='cell']")

        queries = list()
        for cell in cells[1:]:
            query = dict()
            box = cell.find("a", href=True)
            query['id'] = box['href'][17:]
            query['href'] = box['href']
            query['description'] = box.text
            queries.append(query)

        return queries

    def get_news_contents(self, queries, sleep=2):
        """Get news content

        Args:
            queries(list): news list retrieved from `query_news()`
            sleep(int): interval between data scraping(unit: second)

        Returns:
            list: news, length is same as the queries
        """
        BASE_URL = "https://minkabu.jp"

        news_list = list()
        for query in queries:
            news = dict()
            url = BASE_URL + query['href']
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            title = soup.select("div[class='md_index_article fsize_l']")[
                0].get_text('\n').strip()
            publish_time = soup.select("div[class='flr']")[
                0].get_text('\n').strip()[3:]
            article = soup.select("div[class='md_box fsize_m md_normalize']")[
                0].get_text('\n').strip()

            news['id'] = query['id']
            news['url'] = url
            news['title'] = title
            news['publish_time'] = publish_time
            news['article'] = article

            news_list.append(news)

            time.sleep(sleep)

        return news_list
