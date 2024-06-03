# Financial Data Scraper
A collection of functions used to scrape financial data, together with financial indicators calculator such as *RSI*, *beta*, *MACD*, etc.

## Getting Started
* Install the package

      pip install fscraper
* Import the package  

      import fscraper as fs

## Kabutan(株探)
- Get the minutes stock price
```python
kt = fs.KabutanScraper('7203.T')
df = kt.get_stock_price_by_minutes()
```
## Kabuyoho(株予報)
- Get the predicted target price
```python
ky = fs.KabuyohoScraper('7203.T')
df = ky.get_target_price()
```

## Minkabu(みんかぶ)
Initialize with
```python
    mk = fs.MinkabuScraper('7203.T')
```
- Get the `Minkabu` analytic data for the recent 1 year including *target price*, *predict price* and *theoretical price*, etc.
```python
df = mk.get_analysis()
```
- Get the corresponding ticker code's news abstract
```python
queries = ms.get_news_abstract()
```
- Get the news contents
```python
news_list = ms.get_news_contents(queries)
```

## Yahoo! Finance
- Get the stock price   
```python
yfs = fs.YahooFinanceScraper('7203.T')
df = yfs.get_stock_price(period='10y', interval='1d')
df = yfs.get_stock_price2(start='2010-01-01', end='2020-12-12')
```


!!! note "Title"

    Some note

