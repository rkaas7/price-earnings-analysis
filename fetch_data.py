import yfinance as yf
from datetime import datetime, timedelta

def fetch_pe_data(symbol):
    ticker = yf.Ticker(symbol)

    try:
        info = ticker.info
        name = info.get('shortName', symbol)
        current_pe = info.get('trailingPE', None)
        eps = info.get('trailingEps', None)
    except:
        name = symbol
        current_pe, eps = None, None

    pe_ratios = []
    end = datetime.today()

    for i in range(10):
        year_end = end.replace(year=end.year - i)
        try:
            hist = ticker.history(period='1y', end=year_end)
            if not hist.empty and eps:
                avg_price = hist['Close'].mean()
                pe = avg_price / eps
                pe_ratios.append(pe)
        except:
            continue

    avg_pe_10y = sum(pe_ratios) / len(pe_ratios) if pe_ratios else None

    return {
        "symbol": symbol,
        "name": name,
        "current_pe": current_pe,
        "avg_pe_10y": avg_pe_10y
    }