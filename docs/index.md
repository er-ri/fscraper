# Financial Data Scraper
The project contains a collection of functions used to scrape financial data, together with financial indicators calculator such as *RSI*, *beta*, *MACD*, etc.

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

## Financial Indicator
```python
# RSI
df['rsi'] = fs.calculate_rsi(df['close'])
df['rsi'] = fs.calculate_rsi(df['close'], periods=14)

# Stochastic Oscillator Index
df['%K'], df['%D'] = fs.calculate_stochastic_oscillator(df['high'], df['low'], df['close'])
df['%K'], df['%D'] = fs.calculate_stochastic_oscillator(df['high'], df['low'], df['close'], k_period=14, d_period=3)

# Bollinger Band
df['top'], df['bottom'] = fs.calculate_bollinger_bands(df['close'])
df['top'], df['bottom'] = fs.calculate_bollinger_bands(df['close'], smooth_period=20, standard_deviation=2)

# MACD(Moving Average Convergence/Divergence)
df['macd'], df['macd_signal'], df['macd_histogram'] = fs.calculate_macd(df['close'])
df['macd'], df['macd_signal'], df['macd_histogram'] = fs.calculate_macd(df['close'], short_periods=12, long_periods=26, signal_periods=9)

# Pearson Correlation
cor = fs.calculate_pearson_correlation(df1['close'], df2['close'])

# beta with Nikkei 225
beta = fs.calculate_beta(code='6753.T', market='^N225', period='1y')

# 100 days min&max price
df['100-high'], df['100-low'] = fs.set_x_days_high_low(df['high'], df['low'], window=100)

# On Balance Volume (OBV)
df['OBV'] = fs.calculate_obv(df['close'], df['volume'])
```
