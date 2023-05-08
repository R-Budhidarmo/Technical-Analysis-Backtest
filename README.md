# Strategy 1: MACD-RSI-Strategy

This Jupyter notebook contains an example of how a simple algorithmic trading strategy based on MACD (Moving Average Converge Divergence) and RSI (Relative Strength Index) can be implemented for backtesting and to calculate the expected returns.
<br>
<br> The strategy is as follows:
- Buy Signal: RSI > 30 and MACD histogram > 0
- Sell Signal: RSI < 70 or MACD histogram < 0

# Strategy 2: SMA-MACD-Strategy-withSL

This 2nd example is another simple algorithmic trading strategy based on SMA (Simple Moving Average) and MACD (Moving Average Converge Divergence). This is a continuation from the previous MACD-RSI-based strategy above.
Here, Stop Losses (SL) and Target Profits (TP) are also used to define our exits. The SL and TP are set based on the Average True Range (ATR) value upon entry.

The strategy is as follows:
- Entry Signal: Close Price > SMA200 and MACD histogram > 0
- Exit Signal: when the SL or TP are hit
- SL = entry price - 2 * entry ATR
- TP = entry price + 3 * entry ATR

As an example, the strategies have been applied on the daily share price data from 2018 - 2023 scraped from Yahoo Finance for GlaxoSmithKline stock ([GSK.L](https://uk.finance.yahoo.com/quote/GSK.L/history/)) (as listed on the London Stock Exchange). In this 2nd example, we are only going to go long when a signal arises & sell when our SL or TP is hit (we're not going to short anything at this point). Fees, spread and slippage have not been accounted for.

**Disclaimer:**
- This code is for *educational purposes only*. Please do your own due diligence & trade at your own discretion. The code can be used a starting point to develop more advanced backtesting strategies, but please don't use it in its current form to execute real trades in the financial markets using your own hard-earned cash (or, worse, someone else's cash).
