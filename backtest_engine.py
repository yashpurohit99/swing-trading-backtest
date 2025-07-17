import pandas as pd

def backtest(signals, capital=100000, risk_per_trade=0.01):
    trades = []
    buy_trade = None

    for _, row in signals.iterrows():
        if row['Signal'] == 'BUY':
            buy_trade = row
        elif row['Signal'] == 'SELL' and buy_trade is not None:
            entry_price = buy_trade['Price']
            exit_price = row['Price']
            quantity = capital * risk_per_trade / abs(entry_price - buy_trade['Stop_Loss']) if 'Stop_Loss' in buy_trade else 1
            quantity = max(int(quantity), 1)

            pnl = (exit_price - entry_price) * quantity
            return_pct = ((exit_price - entry_price) / entry_price) * 100
            duration = (row['Date'] - buy_trade['Date']).days if isinstance(row['Date'], pd.Timestamp) else 0

            trades.append({
                'Buy_Date': buy_trade['Date'],
                'Sell_Date': row['Date'],
                'Buy_Price': entry_price,
                'Sell_Price': exit_price,
                'Quantity': quantity,
                'PnL': pnl,
                'Return_%': return_pct,
                'Days_in_Trade': duration
            })
            buy_trade = None

    df = pd.DataFrame(trades)
    return df


