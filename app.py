import dash
from dash import html, dcc
import plotly.graph_objs as go

from read_yaml import read_stock_symbols
from fetch_data import fetch_pe_data

app = dash.Dash(__name__)
app.title = "KGV Analyse"

symbols = read_stock_symbols()
data = [fetch_pe_data(sym) for sym in symbols]

def safe_value(v):
    return max(0, round(v, 2)) if isinstance(v, (int, float)) else 0

def create_company_card(entry):
    # Immer 3 Balken anzeigen, auch wenn Werte fehlen
    fig = go.Figure(data=[
        go.Bar(name='Trailing PE', x=[''], y=[safe_value(entry.get('trailing_pe'))], marker_color='blue'),
        go.Bar(name='Forward PE', x=[''], y=[safe_value(entry.get('forward_pe'))], marker_color='orange'),
        go.Bar(name='10y Avg PE', x=[''], y=[safe_value(entry.get('avg_pe_10y'))], marker_color='green')
    ])

    fig.update_layout(
        barmode='group',
        title=entry.get('name', entry.get('symbol', 'Unbekannt')),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        yaxis_title="KGV"
    )

    return html.Div(
        dcc.Graph(figure=fig),
        style={'width': '19%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}
    )

app.layout = html.Div([
    html.H1("KGV Vergleich: Trailing, Forward und 10-Jahres-Durchschnitt"),
    html.Div([create_company_card(entry) for entry in data])
])

if __name__ == '__main__':
    app.run(debug=True)
