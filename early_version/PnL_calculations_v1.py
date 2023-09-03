import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def PnL_long(data, buy_price, sell_price, initial_investment, size_per_trade, leverage):

    # copy df (a checkpoint) for P&L calculations
    df2 = data.copy()

    # generate a dataframe containing all buy transactions (Date & Price)
    buy_df = pd.DataFrame({'Buy Date': df2.index, 'Buy Price': buy_price})
    buy_df.dropna(inplace=True)
    buy_df.reset_index(inplace=True)
    buy_df.drop(columns='index', axis=1, inplace=True)

    # generate a dataframe containing all sell transactions (Date & Price)
    sell_df = pd.DataFrame({'Sell Date': df2.index, 'Sell Price': sell_price})
    sell_df.dropna(inplace=True)
    sell_df.reset_index(inplace=True)
    sell_df.drop(columns='index', axis=1, inplace=True)

    # If the last buy transaction is not closed, we'll assume that it's closed by the end of the period
    if sell_df.shape[0] < buy_df.shape[0]:
        last_price = pd.DataFrame({'Sell Date': [df2.index[-1]], 'Sell Price': [df2.iloc[-1,3].copy()]})
        sell_df = pd.concat([sell_df, last_price], ignore_index = True)
        sell_df.reset_index()
    
    # generate a new dataframe to compile all buy & sell transactions
    transactions = pd.concat([buy_df, sell_df], axis=1)
    transactions['Net Price Change'] = transactions['Sell Price'] - transactions['Buy Price']
    transactions['Holding Period (Days)'] = transactions['Sell Date'] - transactions['Buy Date']
    transactions['Holding Period (Days)'] = transactions['Holding Period (Days)'].dt.days.astype('int16')

    # calculate the number of units of stocks bought for every trade with and without leverage
    transactions['Units Bought'] = size_per_trade / transactions['Buy Price']
    transactions['Units Bought_leveraged'] = (size_per_trade * leverage) / transactions['Buy Price']

    # calculate P/L per trade
    transactions['PnL'] = (transactions['Sell Price'] * transactions['Units Bought']) - size_per_trade
    transactions['PnL_leveraged'] = (transactions['Sell Price'] * transactions['Units Bought_leveraged']) - (size_per_trade * leverage)

    # calculate cumulative P/L over time
    transactions['Cumul_PnL'] = transactions['PnL'].cumsum()
    transactions['Cumul_PnL_leveraged'] = transactions['PnL_leveraged'].cumsum()

    # calculate the capital growth over time
    transactions['Investment_Value'] = initial_investment + transactions['Cumul_PnL']
    transactions['Investment_Value_leveraged'] = initial_investment + transactions['Cumul_PnL_leveraged']
    
    # Calculate and print the overall statistics

    print('SUMMARY STATISTICS')
    print('---------------------------------------------------------------------------------')

    # count the total number of buy trades & average holding perios
    print(f"Total number of trades: \t \t \t {transactions.shape[0]}")
    print(f"Average holding period (days): \t \t \t {round(transactions['Holding Period (Days)'].mean(), 2)}")

    # calculate the average winning & losing trades and the win rate of the strategy
    positive_hit = [i for i in transactions['PnL_leveraged'] if i > 0]
    negative_hit = [i for i in transactions['PnL_leveraged'] if i < 0]

    mean_positive_hit = sum(positive_hit) / len(positive_hit)
    mean_negative_hit = sum(negative_hit) / len(negative_hit)
    win_rate = len(positive_hit) / transactions.shape[0]

    print(f'Average win size: \t \t \t \t {round(mean_positive_hit,2)}')
    print(f'Average loss size: \t \t \t \t {round(mean_negative_hit,2)}')
    print(f'Win rate of the strategy: \t \t \t {round(win_rate * 100,2)} %')
    print(f'Reward-to-Risk ratio: \t \t \t \t {round(np.absolute(mean_positive_hit / mean_negative_hit),2)}')

    # determine the expectancy of the strategy
    expectancy = (win_rate * mean_positive_hit) - ((1 - win_rate) * mean_negative_hit)

    print(f'Expectancy of the strategy: \t \t \t {round(expectancy,2)}')

    if expectancy > 0:
        print('The strategy has a POSITIVE expectancy')
    elif expectancy < 0:
        print('The strategy has a NEGATIVE expectancy')
    else:
        print('The strategy has a NEUTRAL expectancy')

    print('---------------------------------------------------------------------------------')

    # drawdown calculations
    drawdown = round(transactions['Cumul_PnL'].min(), 2)
    drawdown_leveraged = round(transactions['Cumul_PnL_leveraged'].min(), 2)

    print(f'Maximum drawdown (without using leverage): \t \t \t {drawdown}')
    print(f'Maximum drawdown (with {leverage} x leverage): \t \t \t \t {drawdown_leveraged}')
    print('---------------------------------------------------------------------------------')

    # calculations of capital value by the end of period
    end_value = round(initial_investment + (transactions['PnL'].sum()), 2)
    end_value_leveraged = round(initial_investment + (transactions['PnL_leveraged'].sum()), 2)

    # calculations of percent gained / lost by the end of period
    pct_end_gain = round(((transactions['Cumul_PnL'].iloc[-1]) / initial_investment) * 100, 2)
    pct_end_gain_leveraged = round(((transactions['Cumul_PnL_leveraged'].iloc[-1]) / initial_investment) * 100, 2)

    # Calculations of buy-and-hold (BH) strategy P/L
    BH_entry_price = df2['Close'].iloc[0]
    BH_exit_price = df2['Close'].iloc[-1]

    BH_no_of_units = (initial_investment * 100) / BH_entry_price
    BH_end_value = round((BH_exit_price * BH_no_of_units) / 100, 2)
    BH_pct_end_gain = round(((BH_end_value - initial_investment) / initial_investment) * 100, 2)

    print(f'Percent gain or loss by the end of period (without leverage): \t {pct_end_gain} %')
    print(f'Percent gain or loss by the end of period (with {leverage} x leverage):\t {pct_end_gain_leveraged} %')
    print(f'Percent gain or loss by the end of period (buy-and-hold): \t {BH_pct_end_gain} %')
    print('---------------------------------------------------------------------------------')
    print(f'Capital value by the end of period (without leverage): \t \t {end_value}')
    print(f'Capital value by the end of period (with {leverage} x leverage): \t {end_value_leveraged}')
    print(f'Capital value by the end of period (buy-and-hold): \t \t {BH_end_value}')

    # Plot the equity overlaid on the price chart
    fig, ax1 = plt.subplots(figsize=(8,6))
    ax1.scatter(x = transactions['Sell Date'], y = transactions['Investment_Value_leveraged'], color = 'forestgreen')
    ax1.set_ylabel(f'Equity (USD) - with {leverage} x Leverage')
    ax1.tick_params(axis='y', labelcolor='forestgreen')
    ax2 = ax1.twinx()
    ax2.plot(df2['Close'], c='grey', alpha=0.5)
    ax2.set_ylabel('Close Price (USD)')
    ax2.tick_params(axis='y', labelcolor='grey')
    fig.tight_layout()
    plt.title('Capital Value Post Exit')
    plt.show()