# This file contains functions for various common technical analysis indicators for analyses of time series data for stocks, forex or other securities.
# The dataset needs to have the usual OHLC (Open, High, Low, CLose) data, of course.
# I know there are other great Python libraries for TA indicators, 
# but here I worked out most of the functions myself from scratch as a coding exercise.
# So, this is still definitely a work in progress and should not be used to execute actual trades in the financial markets.

import numpy as np

# Bolinger Bands

def bollinger_bands(data, window_size):

    rolling_mean = data['Close'].rolling(window = window_size).mean() #SMA
    rolling_std = data['Close'].rolling(window = window_size).std()
    data['UpperBand'] = rolling_mean + (2*rolling_std)
    data['LowerBand'] = rolling_mean - (2*rolling_std)

    return data

# Relative Strength Index (RSI)

def RSI(data, window):

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = np.absolute(delta.where(delta < 0, 0))
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    RS = avg_gain / avg_loss
    RSI = 100 - (100/(1 + RS))
    data['RSI'] = RSI
    data['Overbought'] = 70
    data['Oversold'] = 30
    
    return data

# Exponential Moving Averages (EMA)

def EMA(data, period):
   
    data[f'EMA{period}'] = data['Close'].ewm(span=period, adjust=False, min_periods=period).mean()

    return(data)

# Weighted Moving Average (WMA)

def WMA(data, period):

    data[f'WMA{period}'] = ''

    for i in range(len(data)):
        wma_numerator = []
        for j in range(period):
            x = (period - j) * data['Close'][i - j]
            wma_numerator.append(x)
        data.iloc[i,-1] = sum(wma_numerator) / (period * (period + 1) / 2)
    
    data.iloc[0:period-1, -1] = np.nan

    return(data)

# Moving Averages Convergence / Divergence (MACD)

def MACD(data):

    slow_ema = 26
    fast_ema = 12
    smooth_ema = 9

    data['slow_EMA'] = data['Close'].ewm(span=slow_ema, adjust=False, min_periods=slow_ema).mean()
    data['fast_EMA'] = data['Close'].ewm(span=fast_ema, adjust=False, min_periods=fast_ema).mean()

    data['MACD'] = data['fast_EMA'] - data['slow_EMA']
    data['Signal'] = data['MACD'].ewm(span=smooth_ema, adjust=False, min_periods=smooth_ema).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal']

    return(data)

# Average True Range (ATR)

def ATR(data, period):
    
    data['High_Low'] = data['High'] - data['Low']
    data['High_Close'] = np.absolute(data['High'] - data['Close'].shift(1))
    data['Low_Close'] = np.absolute(data['Low'] - data['Close'].shift(1))
    data['True_Range'] = data[['High_Low', 'High_Close', 'Low_Close']].max(axis=1)
    data['ATR'] = data['True_Range'].rolling(window = period, min_periods = period).mean()

    return(data)

# SuperTrend

def super_trend(data, multiplier, window):

    data['Median_Price'] = (data['High'] + data['Low'])/2
    data['DownBand'] = data['Median_Price'] - (multiplier * data['ATR'])
    data['DownMax'] = data['DownBand'].rolling(window, min_periods=window).max()
    data['UpBand'] = data['Median_Price'] + (multiplier * data['ATR'])
    data['UpMin'] = data['UpBand'].rolling(window, min_periods=window).min()

    data['Super_Bottom'] = data['DownMax'].copy()
    for i in range(len(data)):
        if data['Close'][i] < data['Super_Bottom'][i]:
            data.iloc[i,-1] = np.nan
        elif data['Super_Bottom'][i] < data['Super_Bottom'][i-1] and (data['Super_Bottom'][i] < data['Close'][i]):
            data.iloc[i,-1] = data.iloc[i-1,-1]
            if data['Close'][i] < data['Super_Bottom'][i]:
                data.iloc[i,-1] = np.nan
    data['Super_Bottom'].ffill(inplace=True)

    data['Super_Top'] = data['UpMin'].copy()
    for i in range(len(data)):
        if data['Close'][i] > data['Super_Top'][i]:
            data.iloc[i,-1] = np.nan
        elif data['Super_Top'][i] > data['Super_Top'][i-1] and (data['Super_Top'][i] > data['Close'][i]):
            data.iloc[i,-1] = data.iloc[i-1,-1]
            if data['Close'][i] > data['Super_Top'][i]:
                data.iloc[i,-1] = np.nan
    data['Super_Top'].ffill(inplace=True)

    data['Top_or_Bottom'] = ''
    for i in range(len(data)):
        if (data['Close'][i] > data['Super_Bottom'][i]) and (data['Close'][i] > data['Super_Top'][i]):
            data.iloc[i,-1] = 'Bottom'
        elif (data['Close'][i] < data['Super_Bottom'][i]) and (data['Close'][i] < data['Super_Top'][i]):
            data.iloc[i,-1] = 'Top'
        else:
            data.iloc[i,-1] = np.nan
    data['Top_or_Bottom'].fillna(method='ffill', inplace=True)
    data['Top_or_Bottom'].fillna(method='bfill', inplace=True)

    data['SuperTrend'] = ''
    for i in range(len(data)):
        line = data['Top_or_Bottom'][i]
        data.iloc[i,-1] = data[f'Super_{line}'].iloc[i]

    return (data)

# Chaikin Money Flow (CMF)

def CMF(data, period):
    
    data['CMF_multiplier'] = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
    data['CMF_Vol'] = data['CMF_multiplier'] * data['Volume']
    data['CMF'] = (data['CMF_Vol'].rolling(window = period, min_periods = period).sum()) / (data['Volume'].rolling(window = period, min_periods = period).sum())

    return data

# Choppiness Index (CHOP)

def CHOP(data, period):

    data['Sum_TR'] = data['True_Range'].rolling(window = period, min_periods = period).sum()
    data['Max_High'] = data['High'].rolling(window = period, min_periods = period).max()
    data['Min_Low'] = data['Low'].rolling(window = period, min_periods = period).min()
    data['CHOP'] = 100 * np.log10(data['Sum_TR']/(data['Max_High'] - data['Min_Low'])) / np.log10(period)

    return data

# Vortex Indicator (VI)

def VI(data, period):

    data['VM+']= np.absolute(data['High'] - data['Low'].shift(1))
    data['VM-']= np.absolute(data['Low'] - data['High'].shift(1))
    data['VM+_sum'] = data['VM+'].rolling(window = period, min_periods = period).sum()
    data['VM-_sum'] = data['VM-'].rolling(window = period, min_periods = period).sum()
    data['Sum_TR2'] = data['True_Range'].rolling(window = period, min_periods = period).sum()
    data['VI+'] = data['VM+_sum'] / data['Sum_TR2']
    data['VI-'] = data['VM-_sum'] / data['Sum_TR2']

    return(data)
