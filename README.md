# MACD-RSI-Strategy

The Jupyter notebook contains an example of how a simple algorithmic trading strategy based on MACD (Moving Average Converge Divergence) and RSI (Relative Strength Index) can be implemented for backtesting and to calculate the expected returns.
<br>
<br> The strategy is as follows:
- Buy Signal: RSI > 30 and MACD histogram > 0
- Sell Signal: RSI < 70 or MACD histogram < 0

As an example, the strategy will be applied on the daily share price data for GlaxoSmithKline (GSK) stock (as listed on the London Stock Exchange) covering a period from April 2018  -  2023 (approximately a 5-year period. The data were downloaded from Yahoo Finance as a csv file to keep things simple for now).

**Note:**
- I share my code here for *educational purposes only*. The code can be used a starting point to develop more advanced backtesting strategies, but please don't use it in its current form to execute real trades in the financial markets using your own hard-earned cash (or, worse, someone else's cash).
- In this simple strategy, we are only going to go long when a signal arises & sell at the appropriate time (we're not going to short anything at this point). Fees, spread and slippage have not been accounted for. Please do your own due diligence.
