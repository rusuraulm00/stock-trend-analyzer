# Stock Trend Analysis Project

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import talib


class StockAnalyzer:
    def __init__(self, ticker, start_date=None, end_date=None):
        """
        Initialize the StockAnalyzer with a ticker symbol and date range.

        Parameters:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        start_date (str): Start date in 'YYYY-MM-DD' format (default: 1 year ago)
        end_date (str): End date in 'YYYY-MM-DD' format (default: today)
        """
        self.ticker = ticker

        if end_date is None:
            self.end_date = datetime.now()
        else:
            self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

        if start_date is None:
            self.start_date = self.end_date - timedelta(days=365)
        else:
            self.start_date = datetime.strptime(start_date, '%Y-%m-%d')

        self.data = None

    def fetch_data(self):
        """Download historical stock data using yfinance"""
        try:
            ticker_data = yf.Ticker(self.ticker)
            self.data = ticker_data.history(
                start=self.start_date.strftime('%Y-%m-%d'),
                end=self.end_date.strftime('%Y-%m-%d')
            )
            print(f"Downloaded {len(self.data)} records for {self.ticker}")
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False

    def calculate_indicators(self):
        """Calculate technical indicators using TA-Lib"""
        if self.data is None or len(self.data) < 50:
            print("Insufficient data for technical analysis")
            return False

        # Calculate moving averages
        self.data['SMA20'] = talib.SMA(self.data['Close'], timeperiod=20)
        self.data['SMA50'] = talib.SMA(self.data['Close'], timeperiod=50)
        self.data['SMA200'] = talib.SMA(self.data['Close'], timeperiod=200)

        # Calculate MACD
        macd, macd_signal, macd_hist = talib.MACD(
            self.data['Close'],
            fastperiod=12,
            slowperiod=26,
            signalperiod=9
        )
        self.data['MACD'] = macd
        self.data['MACD_Signal'] = macd_signal
        self.data['MACD_Hist'] = macd_hist

        # Calculate RSI
        self.data['RSI'] = talib.RSI(self.data['Close'], timeperiod=14)

        # Calculate Bollinger Bands
        upper, middle, lower = talib.BBANDS(
            self.data['Close'],
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0
        )
        self.data['BB_Upper'] = upper
        self.data['BB_Middle'] = middle
        self.data['BB_Lower'] = lower

        return True

    def plot_price_and_volume(self):
        """Plot price and volume chart"""
        if self.data is None:
            print("No data available for plotting")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

        # Plot price and moving averages
        ax1.set_title(f'{self.ticker} Price Chart')
        ax1.plot(self.data.index, self.data['Close'], label='Close Price', color='black')
        ax1.plot(self.data.index, self.data['SMA20'], label='20-day SMA', color='blue')
        ax1.plot(self.data.index, self.data['SMA50'], label='50-day SMA', color='orange')
        ax1.plot(self.data.index, self.data['SMA200'], label='200-day SMA', color='red')
        ax1.fill_between(self.data.index, self.data['BB_Upper'], self.data['BB_Lower'],
                         alpha=0.2, color='gray', label='Bollinger Bands')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True)

        # Plot volume
        ax2.bar(self.data.index, self.data['Volume'], color='blue', alpha=0.5)
        ax2.set_ylabel('Volume')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

    def plot_indicators(self):
        """Plot technical indicators"""
        if self.data is None:
            print("No data available for plotting")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

        # Plot MACD
        ax1.set_title(f'{self.ticker} MACD')
        ax1.plot(self.data.index, self.data['MACD'], label='MACD', color='blue')
        ax1.plot(self.data.index, self.data['MACD_Signal'], label='Signal Line', color='red')
        ax1.bar(self.data.index, self.data['MACD_Hist'], label='Histogram', color='green', alpha=0.5)
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.legend()
        ax1.grid(True)

        # Plot RSI
        ax2.set_title(f'{self.ticker} RSI')
        ax2.plot(self.data.index, self.data['RSI'], label='RSI', color='purple')
        ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5)
        ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5)
        ax2.set_ylabel('RSI')
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

    def analyze_trend(self):
        """Analyze current trend based on technical indicators"""
        if self.data is None or len(self.data) < 200:
            print("Insufficient data for trend analysis")
            return

        # Get most recent values
        latest = self.data.iloc[-1]
        prev = self.data.iloc[-2]

        print(f"\nTrend Analysis for {self.ticker} as of {self.data.index[-1].date()}:")

        # Price relative to moving averages
        price = latest['Close']
        sma20 = latest['SMA20']
        sma50 = latest['SMA50']
        sma200 = latest['SMA200']

        print(f"\nClose Price: ${price:.2f}")

        # Trend based on moving averages
        if price > sma20 > sma50 > sma200:
            print("Strong Uptrend: Price above all major moving averages")
        elif price < sma20 < sma50 < sma200:
            print("Strong Downtrend: Price below all major moving averages")
        elif price > sma200:
            print("Long-term Uptrend: Price above 200-day moving average")
        elif price < sma200:
            print("Long-term Downtrend: Price below 200-day moving average")

        # MACD analysis
        macd = latest['MACD']
        signal = latest['MACD_Signal']
        prev_macd = prev['MACD']
        prev_signal = prev['MACD_Signal']

        print(f"\nMACD: {macd:.3f}")
        print(f"MACD Signal: {signal:.3f}")

        if macd > signal and prev_macd <= prev_signal:
            print("Bullish MACD Crossover: MACD crossed above signal line")
        elif macd < signal and prev_macd >= prev_signal:
            print("Bearish MACD Crossover: MACD crossed below signal line")
        elif macd > signal:
            print("MACD above signal line (bullish momentum)")
        else:
            print("MACD below signal line (bearish momentum)")

        # RSI analysis
        rsi = latest['RSI']
        print(f"\nRSI: {rsi:.2f}")

        if rsi > 70:
            print("Overbought: RSI above 70")
        elif rsi < 30:
            print("Oversold: RSI below 30")
        else:
            print("RSI in neutral territory")

        # Bollinger Bands analysis
        upper_band = latest['BB_Upper']
        lower_band = latest['BB_Lower']

        if price > upper_band:
            print("\nPrice above upper Bollinger Band (potential overbought)")
        elif price < lower_band:
            print("\nPrice below lower Bollinger Band (potential oversold)")
        else:
            print("\nPrice within Bollinger Bands")


def main():
    """Main function to run the stock analysis"""
    print("Stock Trend Analysis Tool")
    print("------------------------")

    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").strip().upper()

    # Get optional date range
    use_custom_dates = input("Use custom date range? (y/n): ").strip().lower() == 'y'

    start_date = None
    end_date = None

    if use_custom_dates:
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD, leave blank for today): ").strip()
        if end_date == "":
            end_date = None

    # Create analyzer and run analysis
    analyzer = StockAnalyzer(ticker, start_date, end_date)

    if analyzer.fetch_data():
        analyzer.calculate_indicators()

        # Show analysis options
        print("\nAnalysis Options:")
        print("1. Show price and volume chart")
        print("2. Show technical indicators")
        print("3. Analyze current trend")
        print("4. All of the above")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == '1' or choice == '4':
            analyzer.plot_price_and_volume()

        if choice == '2' or choice == '4':
            analyzer.plot_indicators()

        if choice == '3' or choice == '4':
            analyzer.analyze_trend()

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()