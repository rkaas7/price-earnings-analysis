import yaml

def read_stock_symbols(yaml_file='stocks.yaml'):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
        return data.get("stocks", []) # return all stocks added to watchlist
