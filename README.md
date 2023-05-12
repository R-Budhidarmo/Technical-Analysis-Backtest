# Algorithmic-Trading-Backtest

This is a repository of files that are part of an ongoing project to develop a generic tool for algorithmic / quant trading systems. Examples of the strategies can be found below and more will be developed and added here in the future. Examples of common technical indicators functions in Python can be found [here](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/TA_indicators_v1.py).

**Disclaimer:**
The files and codes here are presented for *educational purposes only*. Please do your own due diligence & trade at your own discretion. The codes can be used a starting point to develop more advanced backtesting strategies, but please don't use them in their current form to execute real trades in the financial markets using your own hard-earned cash (or, worse, someone else's cash). Fees, spread, and slippage have not been accounted for in the models.

### Strategy 1: [MACD-RSI-Strategy](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/MACD_RSI_strategy.ipynb)

This Jupyter notebook contains an example of how a simple algorithmic trading strategy based on MACD (Moving Average Converge Divergence) and RSI (Relative Strength Index) can be implemented for backtesting and to calculate the expected returns.
<br>
- Buy Signal: RSI > 30 and MACD histogram > 0
- Sell Signal: RSI < 70 or MACD histogram < 0

### Strategy 2: [SMA-MACD-Strategy-withSL](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/SMA_MACD_withSL_Strategy.ipynb)

This 2nd example is another simple algorithmic trading strategy based on SMA (Simple Moving Average) and MACD. This is a continuation from strategy 1 above.
Here, Stop Losses (SL) and Target Profits (TP) are also used to define our exits. The SL and TP are set based on the Average True Range (ATR) value upon entry.

- Entry Signal: Close Price > SMA200 and MACD histogram > 0
- Exit Signal: when the SL or TP are hit
- SL = entry price - 2 * entry ATR
- TP = entry price + 3 * entry ATR

In this 2nd strategy, we are only going to go long when a signal arises & sell when our SL or TP is hit (we're not going to short anything at this point).
As an example, the strategies have been applied on the daily share price data from 2018 - 2023 [downloaded](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/GSK.L.csv) or scraped from Yahoo Finance for GlaxoSmithKline stock ([GSK.L](https://uk.finance.yahoo.com/quote/GSK.L/history/)) (as listed on the London Stock Exchange).

### Strategy 3: [EMA_MACD_SuperTrend_strategy](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/EMA_MACD_SuperTrend_strategy.ipynb)

This 3rd example shows how a strategy based on EMA (Exponential Moving Average), MACD (Moving Average Converge Divergence) and the SuperTrend indicator can be implemented for backtesting and to calculate the expected P & L (this strategy is a continuation from strategy 2 above).

- Entry Signal: Close Price > EMA200, MACD histogram > 0, Close Price > SuperTrend
- Exit Signal: Close Price < SuperTrend

### Strategy 4: [WMA_VI_CMF_CHOP_SuperTrend_strategy](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/WMA_VI_CMF_CHOP_SuperTrend_strategy.ipynb)

In this 4th example, an entirely different set of indicators were employed - WMA (Weighted Moving Average), VI (Vortex Indicator), CMF (Chaikin Money Flow), CHOP (Choppiness Index), and the SuperTrend indicators - to compare it to strategy 3.

- Entry Signal: Close Price > WMA200, +VI > 1, CMF > 0, CHOP < 50, Close Price > SuperTrend
- Exit Signal: Close Price < SuperTrend

*For strategy 3 and 4 only:*
The ATR (Average True Range)-based SuperTrend indicator was also used as a trailing Stop Losses (SL) to define our exits. The strategies were be applied on the daily price data from 2018 - 2023 scraped from Yahoo Finance for a Silver ETF (iShares Silver Trust) ([SLV](https://uk.finance.yahoo.com/quote/SLV)). The functions for the various indicators can be found in a file named ['TA_indicators_v1.py'](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/TA_indicators_v1.py) in this repo. The function to calculate the P & L, generate a summary table & chart can be in a file named ['PnL_calculations_v1.py'](https://github.com/R-Budhidarmo/Algorithmic-Trading-Backtest/blob/main/PnL_calculations_v1.py) in this repo.

**More strategy examples to follow in the future**
