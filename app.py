import dash
from dash import html, dcc
import plotly.graph_objs as go

from read_yaml import read_stock_symbols
from fetch_data import fetch_pe_data

app = dash.Dash(__name__)
app.title = "KGV Analyse"

symbols = read_stock_symbols()
data = [fetch_pe_data(sym) for sym in symbols]

# Karten-Layout: max. 5 pro Zeile
def create_company_card(entry):
    fig = go.Figure(data=[
        go.Bar(name='Aktuelles KGV', x=[''], y=[entry['current_pe']]),
        go.Bar(name='10-Jahres-Durchschnitt KGV', x=[''], y=[entry['avg_pe_10y']])
    ])
    fig.update_layout(
        barmode='group',
        title=entry['name'],
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        yaxis_title="KGV"
    )

    return html.Div(
        dcc.Graph(figure=fig),
        style={'width': '19%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}
    )

# Layout
app.layout = html.Div([
    html.H1("KGV Vergleich: Aktuell vs. 10-Jahres-Durchschnitt"),
    html.Div([create_company_card(entry) for entry in data])
])

if __name__ == '__main__':
    app.run(debug=True)
