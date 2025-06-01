import yfinance as yf
from datetime import datetime
from macrotrends_scraper import fetch_10y_avg_pe

def fetch_pe_data(stock):
    """
    description: return price earning ratio (trailing, forward, 10-year avg. from yahoo finance for given stock (ticker symbol) )sym
    input:
        - symbol: ticker symbol of single company
    return:
        - dict: (symbol, name, trailing_pe, forward_pe, 10-year-avg.)
    """

    #using yfinance to get data
    symbol = stock['symbol']
    ticker = yf.Ticker(symbol)
    
    info = ticker.info
    name = stock.get('name', info.get('longName', symbol)) # use manually added name, or get by api via symbol
    
    try:
        trailing_pe = info.get('trailingPE', None)
        forward_pe = info.get('forwardPE', None)
        eps = info.get('trailingEps', None)

    except Exception as e:
        return {
            "symbol": symbol,
            "name": name,
            "trailing_pe": None,
            "forward_pe": None,
            "longterm_avg_pe": None,
            "error": f"could not load data: {e}"
        }

    # using manual added historical PE
    longterm_avg_pe = stock.get("long_term_avg_pe")
    
    # estimate historical P/E if it is not manually given ... 
    pe_ratios = []
    
    if longterm_avg_pe is None: # not given, then ...
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

        longterm_avg_pe = sum(pe_ratios) / len(pe_ratios) if pe_ratios else None

    return {
        "symbol": symbol,
        "name": name,
        "trailing_pe": trailing_pe,
        "forward_pe": forward_pe,
        "longterm_avg_pe": longterm_avg_pe,
        "longterm_pe_source": "manually added" if "long_term_avg_pe" in stock else "estimated",
        'sector': stock.get('sector', "Unbekannt"),
        'index': stock.get('index', "Unbekannt")
    }
