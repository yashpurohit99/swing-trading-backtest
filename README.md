# 📈 Swing Trading Backtest Strategy

This project implements a swing trading backtest engine using Python, based on a technical strategy that combines RS55 and RSI indicators across multiple timeframes (Daily and 120-minute). It supports performance analytics, trade reporting, and modular design.

---

## 🚀 Strategy Rules

**Mother Timeframe (Daily):**
- RS55 > 0
- RSI > 50

**Child Timeframe (120-Minute):**
- RS55 > 0
- RSI > 50
- Entry & Exit based on price breakout or retracement

*Note: Currently using Daily timeframe for both signal and entry due to data availability.*

---

## 📊 Features

- Signal generation based on RS55 and RSI
- Modular strategy and backtest logic
- Auto-calculates:
  - PnL per trade
  - Win rate, reward-to-risk ratio, drawdown
- HTML report generation
- Extensible for automation and multiple symbols

---

## 🔧 Tech Stack

- Python
- Pandas, NumPy
- TA-Lib (for indicators)
- Matplotlib/Plotly (for future visualization)
- Jupyter Notebook

---

## 📁 Project Structure
