import time
import unittest
import fscraper as fs
from fscraper.exceptions import CodeNotFound


class TestMethods(unittest.TestCase):

    def tearDown(self):
        time.sleep(1)

    def test_yf_normal(self):
        code = '7203.T'

        yf=fs.YahooFinanceScraper(code=code)
        df = yf.get_stock_price()
        self.assertIsNotNone(df)

    def test_nonexist_code(self):
        """Test delisted code in Yahoo !Finance"""
        code = '8369.T'     # Delisted code

        yf = fs.YahooFinanceScraper(code=code)

        with self.assertRaises(CodeNotFound):
            yf.get_stock_price2(start='2023-12-15')

    def test_reuter_news(self):
        keyword = 'トヨタ自動車'
        news = fs.ReutersScraper.get_news(keyword, 5)
        self.assertEqual(len(news), 5)


    def test_minkabu_news_list(self):
        ms = fs.MinkabuScraper('7203.T')
        queries = ms.query_news()
        time.sleep(2)
        news_list = ms.get_news_list(queries[:3])

        self.assertEqual(len(news_list), 3)

    def test_yfscraper_report(self):
        yf = fs.YahooFinanceScraper('7203.T')
        df = yf.get_financials('cashflow', 'annual')
        self.assertGreater(len(df), 0)


if __name__ == '__main__':
    unittest.main()
