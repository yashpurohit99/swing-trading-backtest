import pandas as pd
import numpy as np

class SwingStrategy:
    def __init__(self, df, benchmark_df, atr_period=14, rsi_period=14, swing_high_period=20):
        # Flatten multi-index if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        if isinstance(benchmark_df.columns, pd.MultiIndex):
            benchmark_df.columns = benchmark_df.columns.droplevel(1)

        self.df = df.copy()
        self.benchmark_df = benchmark_df.copy()
        self.atr_period = atr_period
        self.rsi_period = rsi_period
        self.swing_high_period = swing_high_period

    def calculate_indicators(self):
        self.df['RSI'] = self.compute_rsi(self.df['Close'], self.rsi_period)
        self.df['ATR'] = self.compute_atr(self.df, self.atr_period)
        self.df['Swing_High'] = self.df['High'].rolling(window=self.swing_high_period).max()

        # Align benchmark to stock dates
        self.benchmark_df = self.benchmark_df.reindex(self.df.index)

        stock_return = self.df['Close'].pct_change(55)
        benchmark_return = self.benchmark_df['Close'].pct_change(55)

        rs55 = (stock_return - benchmark_return).reindex(self.df.index)
        self.df['RS55'] = rs55

        # 🔍 DEBUG: Print missing values and a sample of the indicator dataframe
        print("RS55 NaNs:", self.df['RS55'].isna().sum())
        print("RSI NaNs:", self.df['RSI'].isna().sum())
        print("Swing High NaNs:", self.df['Swing_High'].isna().sum())
        print("ATR NaNs:", self.df['ATR'].isna().sum())
        print("\nSample Indicator Data:\n", self.df[['Close', 'RS55', 'RSI', 'Swing_High', 'ATR']].tail(10))

    def generate_signals(self):
        self.calculate_indicators()
        signals = []
        in_trade = False
        entry_price = 0
        stop_loss = 0
        target = 0

        for i in range(1, len(self.df)):
            row = self.df.iloc[i]

            # Entry condition
            if not in_trade:
                if (
                    pd.notna(row['RS55']) and row['RS55'] > -0.02 and
                    pd.notna(row['RSI']) and row['RSI'] > 40 and
                    pd.notna(row['Swing_High']) and row['Close'] > row['Swing_High'] * 0.98
                ):
                    entry_price = row['Close']
                    atr = row['ATR']
                    stop_loss = entry_price - atr * 1.0
                    target = entry_price + atr * 2.0
                    in_trade = True
                    signals.append({
                        'Date': row.name,
                        'Signal': 'BUY',
                        'Price': entry_price,
                        'Stop_Loss': stop_loss,
                        'Target': target
                    })
            else:
                if (
                    pd.notna(row['RSI']) and (
                        row['RSI'] < 50 or row['Close'] < stop_loss
                    )
                ):
                    in_trade = False
                    signals.append({
                        'Date': row.name,
                        'Signal': 'SELL',
                        'Price': row['Close']
                    })

        return pd.DataFrame(signals)

    @staticmethod
    def compute_rsi(series, period=14):
        delta = series.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def compute_atr(df, period=14):
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
