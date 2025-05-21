import yaml

def read_stock_symbols(file_path='stocks.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data.get("stocks", [])
