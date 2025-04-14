# Stock Trend Analyzer

A Python tool for analyzing stock trends using technical indicators.

## Features

- Fetches historical stock data using yfinance
- Calculates and visualizes technical indicators:
  - Simple Moving Averages (20, 50, 200-day)
  - MACD (Moving Average Convergence Divergence)
  - RSI (Relative Strength Index)
  - Bollinger Bands
- Analyzes current trend based on indicators
- Interactive visualizations

## Installation

1. Clone this repository:

git clone https://github.com/rusuraulm00/stock-trend-analyzer
cd stock-trend-analyzer

2. Install dependencies

pip install -r requirements.txt

Note: TA-Lib may require additional installation steps depending on your operating system.
See: https://github.com/mrjbq7/ta-lib for installation instructions.

## Usage

Run the script and follow the prompts:

python stock_analyzer.py

You'll be asked to:

1. Enter a stock ticker symbol (e.g., AAPL)
2. Choose whether to use a custom date range
3. Select analysis options (charts or trend analysis)
