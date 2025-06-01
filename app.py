import dash
from dash import html, dcc
import plotly.graph_objs as go

from read_yaml import read_stock_symbols
from fetch_data import fetch_pe_data



external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
]

DARK_BLUE = '#5D7F99'
DARK_ORANGE = '#D9984F'
DARK_GREEN = '#6FAF6E'

LIGHT_GREY = '#f9f9f9'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "P/E analysis for Lifetime Investments (Trailing P/E, Forward P/E, Longterm avg. P/E)"

symbols = read_stock_symbols()
data = [fetch_pe_data(sym) for sym in symbols]

def safe_value(v):
    return max(0, round(v, 2)) if isinstance(v, (int, float)) else 0

def create_company_card(entry):
    fig = go.Figure(data=[
        go.Bar(name='Trailing PE', x=[''], y=[safe_value(entry.get('trailing_pe'))], marker_color=DARK_BLUE),
        go.Bar(name='Forward PE', x=[''], y=[safe_value(entry.get('forward_pe'))], marker_color= DARK_ORANGE),
        go.Bar(name='Longterm Avg. PE', x=[''], y=[safe_value(entry.get('longterm_avg_pe'))], marker_color=DARK_GREEN)
    ])

    company_name = entry.get('name', entry.get('symbol', 'unknown'))
    source_info = entry.get('longterm_pe_source', '-')

    fig.update_layout(
        barmode='group',
       title={
            'text': f"<b>{company_name}</b><br><span style='font-size:11px; color:gray;'>Longterm PE: {source_info}</span>",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=280,
        margin=dict(l=20, r=20, t=50, b=40),
        plot_bgcolor=LIGHT_GREY,
        paper_bgcolor=LIGHT_GREY,
        font=dict(family='Roboto, sans-serif'),
        yaxis_title="Price / Earnings",
        legend=dict(orientation='h', y=-0.25, x=0.1)
    )

    return html.Div(
        dcc.Graph(figure=fig, config={'displayModeBar': False}),
        style={
            'width': '15%', # 5 cards per line
            'display': 'inline-block',
            'boxShadow': '0 2px 6px rgba(0,0,0,0.08)',
            'borderRadius': '10px',
            'backgroundColor': '#ffffff',
            'padding': '12px',
            'margin': '0.5%',
            'verticalAlign': 'top'
        }
    )

app.layout = html.Div([
    html.H1(app.title, style={
        'fontFamily': 'Roboto, sans-serif',
        'textAlign': 'center',
        'padding': '20px 10px',
        'color': '#333'
    }),
    html.Div(
        [create_company_card(entry) for entry in data],
        style={
            'textAlign': 'center'
        }
    )
], style={
    'fontFamily': 'Roboto, sans-serif',
    'backgroundColor': '#f0f2f5',
    'padding': '20px'
})

if __name__ == '__main__':
    app.run(debug=True)
