import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# the same as long_short_screen_v1_2 but since this is for the multi-stocks backtester,
# there is no equity curves vizualization.

def calculateMaxDD(cumret):
    # Original author: E.P. Chan (Quantitative Trading, 2nd Ed, 2021, Wiley)
    highwatermark=np.zeros(cumret.shape)
    drawdown=np.zeros(cumret.shape)
    drawdownduration=np.zeros(cumret.shape)
    
    for t in np.arange(1, cumret.shape[0]):
        highwatermark[t]=np.maximum(highwatermark[t-1], cumret[t])
        drawdown[t]=(1+cumret[t])/(1+highwatermark[t])-1
        if drawdown[t]==0:
            drawdownduration[t]=0
        else:
            drawdownduration[t]=drawdownduration[t-1]+1
             
    maxDD, i=np.min(drawdown), np.argmin(drawdown) # drawdown < 0 always
    maxDDD=np.max(drawdownduration)
    return maxDD, maxDDD, i

def long_short_screen(data, long_entry_signal, long_exit_signal, short_entry_signal, short_exit_signal, spread, fees):
    df = data.copy()
    
    # ---------- LONG TRADES ----------
    # first, initiate the position tracker (entry & exit signals are generated)
    df['long_tracker'] = ''
    # set position tracker as 1 at entry & set back to 0 upon selling
    df['long_tracker'] = np.where(long_exit_signal, 0, np.nan)
    df['long_tracker'] = np.where(long_entry_signal, 1, df['long_tracker'])
    df['long_tracker'].ffill(inplace=True)
    df['long_tracker'].fillna(0,inplace=True)
    
    # shift the position tracker to reflect a more realistic trading situation
    # i.e. buy & sell the next day after the signal appears (beacuse signals are based on close price)
    df['long_tracker'] = df['long_tracker'].shift()
    df['long_tracker'].fillna(0,inplace=True)
    
    # calculate the percent price change when we're in position
    df['pct_change_long'] = df['long_tracker'] * df['Percent Change']
    df['pct_change_long'].fillna(0,inplace=True)

    # change the pct_change to reflect price change from that day's open to that day's close:
    for i in range(len(df)):
        if (df['long_tracker'][i-1] == 0) and (df['long_tracker'][i] == 1):
            df.iloc[i,-1] = (df['Close'][i] - df['Open'][i])/df['Open'][i]

    # change the pct_change to reflect price change from yesterday's close to today's open (and including the fees):
    for i in range(1,len(df)):
        if (df['long_tracker'][i] == 0) and (df['long_tracker'][i-1] == 1):
            df.iloc[i-1,-1] = ((df['Open'][i-1] - df['Close'][i-2])/df['Close'][i-2]) - spread

    # incorporate fees (financing costs)
    df['pct_change_long'] = np.where(df['long_tracker'] == 1, df['pct_change_long'] - (fees/365),0)

    # calculate the equity curve for long trades
    df['Equity - Long'] = (1 + df['pct_change_long']).cumprod()

    #---------- SHORT TRADES ----------
    # first, initiate the position tracker (entry & exit signals are generated)
    df['short_tracker'] = ''
    # set position tracker as -1 at entry & set back to 0 upon selling
    df['short_tracker'] = np.where(short_exit_signal, 0, np.nan)
    df['short_tracker'] = np.where(short_entry_signal, -1, df['short_tracker'])
    df['short_tracker'].ffill(inplace=True)
    df['short_tracker'].fillna(0,inplace=True)

    # shift the position tracker to reflect a more realistic trading situation
    # i.e. buy & sell the next day after the signal appears (beacuse signals are based on close price)
    df['short_tracker'] = df['short_tracker'].shift()
    df['short_tracker'].fillna(0,inplace=True)

    # calculate the percent price change when we're in position
    df['pct_change_short'] = df['short_tracker'] * df['Percent Change']
    df['pct_change_short'].fillna(0,inplace=True)

    # change the pct_change to reflect price change from that day's open to that day's close:
    for i in range(len(df)):
        if (df['short_tracker'][i-1] == 0) and (df['short_tracker'][i] == -1):
            df.iloc[i,-1] = (df['Close'][i] - df['Open'][i])/df['Open'][i]

    # change the pct_change to reflect price change from yesterday's close to today's open (and including the fees):
    for i in range(1,len(df)):
        if (df['short_tracker'][i] == 0) and (df['short_tracker'][i-1] == -1):
            df.iloc[i-1,-1] = ((df['Open'][i-1] - df['Close'][i-2])/df['Close'][i-2]) - spread

    # incorporate fees (financing costs)
    df['pct_change_short'] = np.where(df['short_tracker'] == -1, df['pct_change_short'] - (fees/365),0)
    
    # calculate equity curve for short trades
    df['Equity - Short'] = (1 + df['pct_change_short']).cumprod()

    df['Equity - Long & Short'] = 0.5 * (df['Equity - Long'] + df['Equity - Short'])

    maxDrawdown, maxDrawdownDuration, maxDrawdownDay=calculateMaxDD(df['Equity - Long & Short'])

    pct_change_net = 0.5 * (df['pct_change_long'] + df['pct_change_short'])
    # excess daily returns = strategy returns - financing cost, assuming risk-free rate of 2.5% & 252 trading days per year
    excessRet = pct_change_net - (0.025/252)
    sharpeRatio = np.sqrt(252) * np.mean(excessRet)/np.std(excessRet)

    cagr = (df['Equity - Long & Short'][-1])**(1/(len(df)/252))-1
    
    return df[['Equity - Long','Equity - Short','Equity - Long & Short']],maxDrawdown, maxDrawdownDuration, str(list(df.index)[maxDrawdownDay])[:10], sharpeRatio, cagr