import time
import unittest
import fscraper as fs
from fscraper.exceptions import CodeNotFoundException, NoArticleFoundException


class TestMethods(unittest.TestCase):

    def test_yf_normal(self):
        code = '7203.T'

        yf=fs.YahooFinanceScraper(code=code)
        df = yf.get_stock_price()
        self.assertIsNotNone(df)

    def test_nonexist_code(self):
        """Test delisted code in Yahoo !Finance"""
        code = '8369.T'     # Delisted code

        yf = fs.YahooFinanceScraper(code=code)

        with self.assertRaises(CodeNotFoundException):
            yf.get_stock_price2(start='2023-12-15')

    def test_reuter_news(self):
        keyword = '7203.T'
        rs = fs.ReutersScraper(keyword)

        news = rs.get_news(keyword, 5)

        self.assertEqual(len(news), 5)

    def test_reuter_news_nofetched(self):
        keyword = 'asdf.T'
        rs = fs.ReutersScraper(keyword)

        with self.assertRaises(NoArticleFoundException):
            rs.get_news(keyword, 5)

    def test_reuter_financial_report(self):
        rs = fs.ReutersScraper('7203.T')
        report = rs.get_financials()

        self.assertEqual(len(report), 10)

    def test_minkabu_news_list(self):
        ms = fs.MinkabuScraper('7203.T')
        queries = ms.query_news()
        time.sleep(2)
        news_list = ms.get_news_list(queries[:3])

        self.assertEqual(len(news_list), 3)

if __name__ == '__main__':
    unittest.main()
