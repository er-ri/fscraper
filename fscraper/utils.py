import pandas as pd
import numpy as np
from .yfscraper import YahooFinanceScraper


def calculate_pearson_correlation(price1: pd.Series, price2: pd.Series):
    """Calculate the Pearson Correlation with the two given prices.

    Args:
        price1(pd.Series): the first price for calculation
        price2(pd.Series): the second price for calculation

    Returns:
        float64: correlation 

    Usage:
        `cor = calculate_pearson_correlation(df1['close'], df2['close'])`
    """
    x = price1.to_numpy()
    y = price2.to_numpy()
    return np.corrcoef(x, y)[1, 0]


def calculate_beta(code: str, market: str = '^N225', period: str = '1y'):
    """Calculate the 'beta' with the given ticker code with the specific period using Yahoo Finance API.

    Args:
        code(str): ticker symbol(e.g. '7203.T')
        period(str): beta of period (e.g. '1d', '1mo'...)

    Returns:
        float64: beta

    Usage:
        `beta = calculate_beta('6753.T', '1y')`
    """
    stock1 = YahooFinanceScraper(code)
    stock2 = YahooFinanceScraper(market)

    df1 = stock1.get_stock_price(period, '1d')
    df2 = stock2.get_stock_price(period, '1d')

    df = pd.concat([df1['close'], df2['close']], axis=1,
                   join='outer', keys=[code, market])

    # Daily returns (percentage returns[`df.pct_change()`] or log returns[`np.log(df/df.shift(1))`])
    daily_returns = df.pct_change()

    cov = daily_returns.cov()[market][code]
    var = daily_returns.var()[market]

    daily_returns = daily_returns.dropna()
    return cov/var


def calculate_rsi(price: pd.Series, periods: int = 14):
    """Calculate RSI(Relative Strength Index) for the given price.

    Note:
        * Greater than 80: overbought, less than 20: oversold. 

    Args:
        price(pd.Series): stock price

    Returns:
        pd.Series: rsi for the date
    """
    # Get up&down moves
    price_delta = price.diff(1)

    # Extract up&down moves amount
    up = price_delta.clip(lower=0)
    down = abs(price_delta.clip(upper=0))

    # Use simple moving average
    sma_up = up.rolling(window=periods).mean()
    sma_down = down.rolling(window=periods).mean()

    # RSI formula
    rs = sma_up / sma_down
    rsi = 100 - (100/(1 + rs))

    return rsi


def calculate_stochastic_oscillator(high: pd.Series, low: pd.Series, close: pd.Series, k_period: int = 14, d_period: int = 3):
    """Calculate Stochastic Oscillator Index('%K' and '%D') for the given price(Dataframe)

    Note:
        * 80: overbought, 20: oversold
        * '%K' crossing below '%D': sell
        * '%K' crossing above '%D': buy

    Args:
        high(pd.Series): stock high price
        low(pd.Series): stock low price
        k_period(int): fast stochastic indicator
        d_period(int): slow stochastic indicator

    Returns:
        pd.Dataframe: input dataframe with 2 more columns'%K' and '%D'
    """
    # Maximum value of previous 14 periods
    k_high = high.rolling(k_period).max()
    # Minimum value of previous 14 periods
    k_low = low.rolling(k_period).min()

    # %K(fast stochastic indicator) formula
    fast = ((close - k_low) / (k_high - k_low)) * 100
    # %D(slow" stochastic indicator)
    slow = fast.rolling(d_period).mean()

    return fast, slow


def calculate_bollinger_bands(close: pd.Series, smooth_period: int = 20, standard_deviation: int = 2):
    """Calculate Bollinger Band for the given stock price.

    Note:
        * Breakouts provide no clue as to the direction and extent of future price movement. 
        * 65% : standard_deviation = 1
        * 95% : standard_deviation = 2
        * 99% : standard_deviation = 3   

    Args:
        close(pd.Series): close price
        smooth_period(int): simple moving average(SMA) period
        standard_deviation(int): standard deviation over last n period

    Returns:
        pd.Dataframe: input dataframe with 2 more columns 'top' and 'bottom'
    """
    sma = close.rolling(smooth_period).mean()
    std = close.rolling(smooth_period).std()

    top = sma + std * standard_deviation  # Calculate top band
    bottom = sma - std * standard_deviation  # Calculate bottom band

    return top, bottom


def calculate_macd(close: pd.Series, short_periods: int = 12, long_periods: int = 26, signal_periods: int = 9):
    """Calculate MACD(Moving Average Convergence/Divergence) using 'close' price.

    Note:
        * MACD Line > Signal Line -> Buy
        * MACD Line < Signal Line -> Sell
        * 'macd_histogram' around 0 indicates a change in trend may occur.

    Args:
        close(pd.Series): close price
        short_periods(int): the short-term exponential moving averages (EMAs)
        long_periods(int): the long-term exponential moving averages (EMAs)
        signal_periods(int): n-period EMA of the MACD line

    Returns:
        pd.Series: macd 
        pd.Series: macd signal
        pd.Series: macd histogram
    """
    # Get the 12-day EMA of the closing price
    short_ema = close.ewm(span=short_periods, adjust=False,
                          min_periods=short_periods).mean()
    # Get the 26-day EMA of the closing price
    long_ema = close.ewm(span=long_periods, adjust=False,
                         min_periods=long_periods).mean()

    # MACD formula: Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = short_ema - long_ema

    # Get the 9-Day EMA of the MACD for the Trigger line singnal line
    macd_signal = macd.ewm(span=signal_periods, adjust=False,
                           min_periods=signal_periods).mean()

    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value histogram
    macd_histogram = macd - macd_signal

    return macd, macd_signal, macd_histogram


def set_x_days_high_low(high: pd.Series, low: pd.Series, window: int):
    """Set x days high/low price.

    Args:
        high(pd.Series): high price
        low(pd.Series): low price
        window(int): window length for high and low price

    Returns:
        pd.Series: highest price for the window
        pd.Series: lowest price for the window

    Usage:
        `df['3-day-high'], df['3-day-low'] = set_x_days_high_low(df['high'], df['low'], window=3)`
    """
    return high.rolling(window=window).max(), low.rolling(window=window).min()


def calculate_obv(close: pd.Series, volume: pd.Series):
    """On Balance Volume (OBV)

    Args:
        close(pd.Series): close price
        volume(pd.Series): day's volume

    Returns:
        pd.Series: OBV

    Usage:
        `df['OBV'] = fs.calculate_obv(df['close'], df['volume'])`
    """
    return (np.sign(close.diff()) * volume).fillna(0).cumsum()
