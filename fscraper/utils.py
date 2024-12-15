# fscraper/utils.py

"""*Provide several functions for calculating Technical Indicators.*
"""

import numpy as np
import pandas as pd
from datetime import datetime


def calculate_pearson_correlation(price1: pd.Series, price2: pd.Series) -> np.float64:
    """Calculate the Pearson Correlation between two given price series.

    Args:
        price1 (pd.Series): The first price series for calculation.
        price2 (pd.Series): The second price series for calculation.

    Returns:
        np.float64: The Pearson correlation coefficient.

    Raises:
        ValueError: If the input series are not of the same length or if they contain NaN values.

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
    """Calculate the beta of a stock relative to a benchmark index over a specified period.

    Args:
        stock (pd.Series): Time series of stock prices.
        index (pd.Series): Time series of benchmark index prices (e.g., 'Nikkei 225': `^N225`, 'S&P 500': `^SPX`).
        start (str): Start date of the period in 'yyyy-mm-dd' format. Defaults to '1985-01-01'.
        end (str): End date of the period in 'yyyy-mm-dd' format. Defaults to today's date.

    Returns:
        np.float64: The calculated beta value.

    Raises:
        ValueError: If the input series are empty or if the dates are invalid.

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
    """Calculate the Relative Strength Index (RSI) for the given price data.

    Args:
        price (pd.Series): A Pandas Series representing stock prices.
        periods (int, optional): The number of periods to use for the RSI calculation. 
            Defaults to 14. Values should be bounded from 0 to 100.

    Returns:
        pd.DataFrame: A DataFrame containing the RSI values.

    Note:
        * RSI values greater than 80 indicate an overbought condition.
        * RSI values less than 20 indicate an oversold condition.
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
    """Calculate Stochastic Oscillator Index('%K' and '%D') for the given price data.

    Args:
        high (pd.Series): Series of stock high prices.
        low (pd.Series): Series of stock low prices.
        close (pd.Series): Series of stock closing prices.
        k_period (int, optional): Period for the fast stochastic indicator. Defaults to 14.
        d_period (int, optional): Period for the slow stochastic indicator. Defaults to 3.

    Returns:
        pd.DataFrame: DataFrame with additional columns '%K' and '%D'.
    
    Note:
        * 80: overbought, 20: oversold
        * '%K' crossing below '%D': sell signal
        * '%K' crossing above '%D': buy signal
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
    """Calculate Bollinger Bands for the given stock price series.

    Args:
        close (pd.Series): A Pandas Series representing the closing prices of a stock.
        smooth_period (int, optional): The period over which to calculate the simple moving average (SMA). Defaults to 20.
        standard_deviation (int, optional): The number of standard deviations to use for the bands. Defaults to 2.

    Returns:
        pd.DataFrame: A DataFrame containing the original closing prices along with two additional columns:
                      'top' for the upper Bollinger Band and 'bottom' for the lower Bollinger Band.

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
    """Calculate the Moving Average Convergence/Divergence (MACD) for a given series of closing prices.

    Args:
        close (pd.Series): Series of closing prices.
        short_periods (int, optional): Number of periods for the short-term EMA. Defaults to 12.
        long_periods (int, optional): Number of periods for the long-term EMA. Defaults to 26.
        signal_periods (int, optional): Number of periods for the signal line EMA. Defaults to 9.

    Returns:
        tuple: A tuple containing three pd.Series:
            - macd: The MACD line.
            - macd_signal: The signal line.
            - macd_histogram: The MACD histogram.

    Notes:
        - When the MACD line crosses above the signal line, it may indicate a buy signal.
        - When the MACD line crosses below the signal line, it may indicate a sell signal.
        - A MACD histogram value around zero suggests a potential change in trend.
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
        high (pd.Series): High prices.
        low (pd.Series): Low prices.
        window (int): Window length for calculating high and low prices.

    Returns:
        tuple[pd.Series, pd.Series]: A tuple containing the highest and lowest prices for the given window.

    Example:
        >>> df['3-day-high'], df['3-day-low'] = get_x_days_high_low(df['high'], df['low'], window=3)
    """
    return high.rolling(window=window).max(), low.rolling(window=window).min()


def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """Calculates the On Balance Volume (OBV).

    Args:
        close (pd.Series): A pandas Series representing the closing prices.
        volume (pd.Series): A pandas Series representing the day's volume.

    Returns:
        pd.Series: A pandas Series containing the calculated OBV values.

    Raises:
        ValueError: If the input series do not have the same length.

    Example:
        >>> df['OBV'] = calculate_obv(df['close'], df['volume'])
    """
    return (np.sign(close.diff()) * volume).fillna(0).cumsum()
