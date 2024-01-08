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


if __name__ == '__main__':
    unittest.main()
