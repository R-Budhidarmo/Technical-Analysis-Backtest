import numpy as np

# Bolinger Bands
def bollinger(data, period=20):
    df = data.copy()
    rolling_mean = df['Close'].rolling(window=period).mean() #SMA
    rolling_std = df['Close'].rolling(window=period).std()
    df['UpperBand'] = rolling_mean + (2*rolling_std)
    df['LowerBand'] = rolling_mean - (2*rolling_std)
    return df[['UpperBand','LowerBand']]

# Relative Strength Index (RSI)
def RSI(data, period=14):
    df = data.copy()
    delta = df['Close'].diff()
    gain = delta.where(delta >= 0, 0)
    loss = abs(delta.where(delta < 0, 0))
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    RS = avg_gain / avg_loss
    df['RSI'] = 100 - (100/(1 + RS))
    return df['RSI']

# Exponential Moving Averages (EMA)
def EMA(data, period=20):
    df = data.copy()
    df[f'EMA{period}'] = df['Close'].ewm(span=period, adjust=False, min_periods=period).mean()
    return df[f'EMA{period}']

# Weighted Moving Average (WMA)
def WMA(data, period=20):
    df = data.copy()
    df[f'WMA{period}'] = ''
    for i in range(len(data)):
        wma_numerator = []
        for j in range(period):
            x = (period - j) * df['Close'][i - j]
            wma_numerator.append(x)
        df.iloc[i,-1] = sum(wma_numerator) / (period * (period + 1) / 2)
    df.iloc[0:period-1, -1] = np.nan
    return df[f'WMA{period}']

# Moving Averages Convergence Divergence (MACD)
def MACD(data, slow = 26, fast = 12, smooth = 9):
    df = data.copy()
    slow_EMA = df['Close'].ewm(span=slow, adjust=False, min_periods=slow).mean()
    fast_EMA = df['Close'].ewm(span=fast, adjust=False, min_periods=fast).mean()
    df['MACD'] = fast_EMA - slow_EMA
    df['Signal'] = df['MACD'].ewm(span=smooth, adjust=False, min_periods=smooth).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    return df[['MACD','Signal','Histogram']]

# Chaikin Money Flow (CMF)
def CMF(data, period):
    df = data.copy()
    cmf_multiplier = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    cmf_volume = cmf_multiplier * df['Volume']
    df['CMF'] = (cmf_volume.rolling(window = period, min_periods = period).sum()) / (df['Volume'].rolling(window = period, min_periods = period).sum())
    return df['CMF']

# Average True Range (ATR)
def ATR(data, period=14):
    df = data.copy()
    df['High_Low'] = df['High'] - df['Low']
    df['High_Close'] = abs(df['High'] - df['Close'].shift(1))
    df['Low_Close'] = abs(df['Low'] - df['Close'].shift(1))
    df['True Range'] = df[['High_Low', 'High_Close', 'Low_Close']].max(axis=1)
    df['ATR'] = df['True Range'].rolling(window = period, min_periods = period).mean()
    return df[['True Range','ATR']]

# Choppiness Index (CHOP)
def CHOP(data, period):
    df = data.copy()
    sum_TR = df['True Range'].rolling(window = period, min_periods = period).sum()
    Max_High = df['High'].rolling(window = period, min_periods = period).max()
    Min_Low = df['Low'].rolling(window = period, min_periods = period).min()
    df['CHOP'] = 100 * np.log10(sum_TR/(Max_High - Min_Low)) / np.log10(period)
    return df['CHOP']

# Vortex Indicator
def vortex(data, period):
    df = data.copy()
    plus_VM = abs(df['High'] - df['Low'].shift(1))
    minus_VM = abs(df['Low'] - df['High'].shift(1))
    plus_VM_sum = plus_VM.rolling(window = period, min_periods = period).sum()
    minus_VM_sum = minus_VM.rolling(window = period, min_periods = period).sum()
    sum_TR = df['True Range'].rolling(window = period, min_periods = period).sum()
    df['VI+'] = plus_VM_sum / sum_TR
    df['VI-'] = minus_VM_sum / sum_TR
    return df[['VI+','VI-']]

# SSL Channel
def SSL(data, period=20):
    df = data.copy()
    df['High SMA'] = df['High'].rolling(window=period).mean()
    df['Low SMA'] = df['Low'].rolling(window=period).mean()
    df['Hi_Lo'] = np.where(
        df['Close'] > df['High SMA'], 1, np.where(df['Close'] < df['Low SMA'], -1, np.nan)
        )
    df['Hi_Lo'] = df['Hi_Lo'].ffill()
    df['SSL Down'] = np.where(df['Hi_Lo'] < 0, df['High SMA'], df['Low SMA'])
    df['SSL Up'] = np.where(df['Hi_Lo'] < 0, df['Low SMA'], df['High SMA'])
    return df[['SSL Down','SSL Up']]

# SuperTrend
def SuperTrend(data, multiplier=3, period=10):
    df = data.copy()
    df[['True Range','ATR']] = ATR(df, period)
    
    Median_Price = (df['High'] + df['Low'])/2

    Down_Band = Median_Price - (multiplier * df['ATR'])
    df['Down_Max'] = Down_Band.rolling(period, min_periods=period).max()

    Up_Band = Median_Price + (multiplier * df['ATR'])
    df['Up_Min'] = Up_Band.rolling(period, min_periods=period).min()

    df['Super_Bottom'] = df['Down_Max'].copy()
    for i in range(len(df)):
        if df['Close'][i] < df['Super_Bottom'][i]:
            df.iloc[i,-1] = np.nan
        elif df['Super_Bottom'][i] < df['Super_Bottom'][i-1] and (df['Super_Bottom'][i] < df['Close'][i]):
            df.iloc[i,-1] = df.iloc[i-1,-1]
            if df['Close'][i] < df['Super_Bottom'][i]:
                df.iloc[i,-1] = np.nan
    df['Super_Bottom'].ffill(inplace=True)

    df['Super_Top'] = df['Up_Min'].copy()
    for i in range(len(df)):
        if df['Close'][i] > df['Super_Top'][i]:
            df.iloc[i,-1] = np.nan
        elif df['Super_Top'][i] > df['Super_Top'][i-1] and (df['Super_Top'][i] > df['Close'][i]):
            df.iloc[i,-1] = df.iloc[i-1,-1]
            if df['Close'][i] > df['Super_Top'][i]:
                df.iloc[i,-1] = np.nan
    df['Super_Top'].ffill(inplace=True)

    df['Top_or_Bottom'] = ''
    for i in range(len(df)):
        if (df['Close'][i] > df['Super_Bottom'][i]) and (df['Close'][i] > df['Super_Top'][i]):
            df.iloc[i,-1] = 'Bottom'
        elif (df['Close'][i] < df['Super_Bottom'][i]) and (df['Close'][i] < df['Super_Top'][i]):
            df.iloc[i,-1] = 'Top'
        else:
            df.iloc[i,-1] = np.nan
    df['Top_or_Bottom'].fillna(method='ffill', inplace=True)
    df['Top_or_Bottom'].fillna(method='bfill', inplace=True)

    df['SuperTrend'] = ''
    for i in range(len(df)):
        line = df['Top_or_Bottom'][i]
        df.iloc[i,-1] = df[f'Super_{line}'].iloc[i]

    return df['SuperTrend']

# On Balance Volume (OBV)
def OBV(data):
    df = data.copy()
    df['daily_ret'] = df['Close'].pct_change()
    df['direction'] = np.where(df['daily_ret']>=0,1,-1)
    df.iloc[0,-1] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['OBV'] = df['vol_adj'].cumsum()
    return df['OBV']

# Average Directional Index (ADX)
def ADX(data, period=14):
    df = data.copy()
    upmove = df['High'] - df['High'].shift(1)
    downmove = df['Low'].shift(1) - df['Low']
    df['+dm'] = np.where((upmove > downmove) & (upmove > 0), upmove, 0)
    df['-dm'] = np.where((downmove > upmove) & (downmove > 0), downmove, 0)
    df['+di'] = 100 * (df['+dm']/df['ATR']).ewm(alpha=1/period, min_periods=period).mean()
    df['-di'] = 100 * (df['-dm']/df['ATR']).ewm(alpha=1/period, min_periods=period).mean()
    df['ADX'] = 100* abs((df['+di'] - df['-di'])/(df['+di'] + df['-di'])).ewm(alpha=1/period, min_periods=period).mean()
    return df['ADX']