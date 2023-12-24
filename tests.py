import unittest
import fscraper as fs
from fscraper.exceptions import CodeNotFoundException


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


if __name__ == '__main__':
    unittest.main()
