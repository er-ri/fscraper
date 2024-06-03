# fscraper/utils.py

"""*Provide several functions for calculating Technical Indicators.*
"""

import numpy as np
import pandas as pd
from datetime import datetime


def calculate_pearson_correlation(price1: pd.Series, price2: pd.Series) -> np.float64:
    """Calculate the Pearson Correlation with the two given prices.

    Args:
        price1: the first price for calculation
        price2: the second price for calculation

    Returns:
        pearson correlation 

    Example:

        >>> cor = calculate_pearson_correlation(df1['close'], df2['close'])

    """
    x = price1.to_numpy()
    y = price2.to_numpy()
    return np.corrcoef(x, y)[1, 0]


def calculate_beta(stock: pd.Series, 
                   index: pd.Series, 
                   start: str='1985-01-01', 
                   end: str=datetime.now().strftime('%Y-%m-%d')) -> np.float64:
    """Calculate the 'beta' with the given ticker code with the specific period using Yahoo Finance API.

    Args:
        stock: stock value
        index: benchmark index('Nikkei 225': `^N225`, 'S&P 500': `^SPX`)
        start: start time period(format: `yyyy-mm-dd`)
        end: end time period(format: `yyyy-mm-dd`)

    Returns:
        beta

    Example:
    
        >>> beta = calculate_beta(stock, index, '2020-01-01', '2024-01-01')

    """
    # Daily returns (percentage returns[`df.pct_change()`] or log returns[`np.log(df/df.shift(1))`])
    stock_returns = stock.pct_change()
    index_returns = index.pct_change()

    df = pd.concat([stock_returns, index_returns], axis=1,
                   join='outer', keys=['Stock Returns', 'Index Returns'])

    df = df.loc[(df.index > start) & (df.index < end)].dropna()

    cov_matrix = df.cov()

    cov = cov_matrix.loc['Stock Returns', 'Index Returns']
    var = cov_matrix.loc['Index Returns', 'Index Returns']

    return cov/var


def calculate_rsi(price: pd.Series, periods: int = 14) -> pd.DataFrame:
    """Calculate RSI(Relative Strength Index) for the given price.

    Args:
        price: stock price
        periods: The default time period, values bounded from 0 to 100

    Returns:
        rsi for the data

    Note:
        * Greater than 80: overbought, less than 20: oversold. 

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


def calculate_stochastic_oscillator(high: pd.Series, 
                                    low: pd.Series, 
                                    close: pd.Series, 
                                    k_period: int = 14, 
                                    d_period: int = 3)->pd.DataFrame:
    """Calculate Stochastic Oscillator Index('%K' and '%D') for the given price(Dataframe)

    Args:
        high: stock high price
        low: stock low price
        k_period: fast stochastic indicator
        d_period: slow stochastic indicator

    Returns:
        Input dataframe with 2 more columns'%K' and '%D'
    
    Note:
        * 80: overbought, 20: oversold
        * '%K' crossing below '%D': sell
        * '%K' crossing above '%D': buy

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


def calculate_bollinger_bands(close: pd.Series, smooth_period: int = 20, standard_deviation: int = 2) -> pd.DataFrame:
    """Calculate Bollinger Band for the given stock price.

    Args:
        close: close price
        smooth_period: simple moving average(SMA) period
        standard_deviation: standard deviation over last n period

    Returns:
        Input dataframe with 2 more columns 'top' and 'bottom'

    Note:
        * Breakouts provide no clue as to the direction and extent of future price movement. 
        * 65% : standard_deviation = 1
        * 95% : standard_deviation = 2
        * 99% : standard_deviation = 3

    """
    sma = close.rolling(smooth_period).mean()
    std = close.rolling(smooth_period).std()

    top = sma + std * standard_deviation  # Calculate top band
    bottom = sma - std * standard_deviation  # Calculate bottom band

    return top, bottom


def calculate_macd(close: pd.Series, short_periods: int = 12, long_periods: int = 26, signal_periods: int = 9) -> tuple:
    """Calculate MACD(Moving Average Convergence/Divergence) using 'close' price.

    Args:
        close: close price
        short_periods: the short-term exponential moving averages (EMAs)
        long_periods: the long-term exponential moving averages (EMAs)
        signal_periods: n-period EMA of the MACD line

    Returns:
        macd: pd.Series
        macd signal: pd.Series
        macd histogram: pd.Series

    Note:
        * MACD Line > Signal Line -> Buy
        * MACD Line < Signal Line -> Sell
        * 'macd_histogram' around 0 indicates a change in trend may occur.

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


def get_x_days_high_low(high: pd.Series, low: pd.Series, window: int) -> tuple:
    """Get x days high/low price.

    Args:
        high: high price
        low: low price
        window: window length for high and low price

    Returns:
        highest price for the window
        lowest price for the window

    Example:

        >>> df['3-day-high'], df['3-day-low'] = get_x_days_high_low(df['high'], df['low'], window=3)

    """
    return high.rolling(window=window).max(), low.rolling(window=window).min()


def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """On Balance Volume (OBV)

    Args:
        close: close price
        volume: day's volume

    Returns:
        OBV

    Example:
        
        >>> df['OBV'] = fs.calculate_obv(df['close'], df['volume'])

    """
    return (np.sign(close.diff()) * volume).fillna(0).cumsum()
