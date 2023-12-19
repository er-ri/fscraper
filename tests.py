import unittest
import fscraper as fs
from fscraper.exceptions import CodeNotFoundException


class TestMethods(unittest.TestCase):

    def test_nonexist_code(self):
        """Test delisted code in Yahoo !Finance"""
        code = '8369.T'     # Delisted code

        yf = fs.YahooFinanceScraper(code=code)
        try:
            yf.get_stock_price2(start='2023-12-15')
        except CodeNotFoundException as e:
            self.assertEqual(
                e.message, "No data found, symbol may be delisted")


if __name__ == '__main__':
    unittest.main()
