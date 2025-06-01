import requests
from bs4 import BeautifulSoup
import re

def fetch_10y_avg_pe(symbol):
    url = f"https://www.macrotrends.net/stocks/charts/{symbol}/{symbol.lower()}/pe-ratio"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"could not load the page: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')

    pe_data = []

    # search for the relevant js
    for script in scripts:
        if "var peRatioData" in script.text:
            matches = re.findall(r'"date":"(\d{4}-\d{2}-\d{2})","v":([\d.]+|null)', script.text)
            for date_str, value_str in matches:
                if value_str != "null":
                    year = int(date_str.split('-')[0])
                    if year >= (2025 - 10):  # last 10 years
                        pe_data.append(float(value_str))
            break

    if pe_data:
        avg_pe = sum(pe_data) / len(pe_data)
        return round(avg_pe, 2)
    else:
        print(f"no historical PE data found for {symbol}")
        return None
