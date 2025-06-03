# 📊 Price/Earnings analysis for Lifetime Investments

This tool provides a clean and insightful web interface to visualize **Price/Earnings ratios (P/E)** of selected companies, helping long-term investors identify **potentially undervalued stocks**.


![image](dashboard.png)

The dashboard displays:

- **Trailing P/E**: Price divided by the most recent 12-month earnings.
- **Forward P/E**: Price divided by projected 12-month earnings.
- **Long-Term Average P/E**: Historical valuation benchmark (manually defined, or estimated by the tool (data not available on yahoo finance) ).

With filters for **index** and **sector**, investors can quickly screen and compare current valuations against historical averages and identify historically cheap companies for further analysis.

**Data is fetched from Yahoo Finance (via yfinance)**

### Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate # on Windows: .venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Add or modify your Watchlist (stocks.yaml)

```yaml 
stocks: 
  - symbol: PG
    name: Procter & Gamble
    long_term_avg_pe: 24.0 # search for long term PE Ratio in the web or let the tool estimate
    sector: Consumer Staples
    index: S&P 500
```

### Run the Dashboard
```bash
python app.py
```
