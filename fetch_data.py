import yfinance as yf
from datetime import datetime

def fetch_pe_data(symbol):
    ticker = yf.Ticker(symbol)

    try:
        info = ticker.info
        name = info.get('shortName', symbol)
        #if symbol == 'BFFAF': 
        #    print(info)

        # Optional: Benchmarks benennen
        if symbol == "SPY":
            name = "S&P 500 (via SPY)"
        elif symbol == "EXS1.DE":
            name = "DAX (via EXS1.DE)"

        trailing_pe = info.get('trailingPE', None)
        forward_pe = info.get('forwardPE', None)
        eps = info.get('trailingEps', None)
    except Exception as e:
        return {
            "symbol": symbol,
            "name": symbol,
            "trailing_pe": None,
            "forward_pe": None,
            "avg_pe_10y": None,
            "error": f"Fehler beim Laden: {e}"
        }

    # Historischer Durchschnitts-KGV aus approximierter Methode
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
        "trailing_pe": trailing_pe,
        "forward_pe": forward_pe,
        "avg_pe_10y": avg_pe_10y
    }
