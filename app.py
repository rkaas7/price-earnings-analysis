import dash
from dash import html, dcc, Input, Output
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

BAR_WIDTH = 0.20

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Price/Earnings analysis for Lifetime Investments"

symbols = read_stock_symbols()
data = [fetch_pe_data(sym) for sym in symbols]

def safe_value(v):
    return max(0, round(v, 2)) if isinstance(v, (int, float)) else 0

def create_company_card(entry):
    fig = go.Figure(data=[
        go.Bar(name='Trailing PE', x=[''], y=[safe_value(entry.get('trailing_pe'))], marker_color=DARK_BLUE, width=BAR_WIDTH),
        go.Bar(name='Forward PE', x=[''], y=[safe_value(entry.get('forward_pe'))], marker_color= DARK_ORANGE, width=BAR_WIDTH),
        go.Bar(name='Longterm Avg. PE', x=[''], y=[safe_value(entry.get('longterm_avg_pe'))], marker_color=DARK_GREEN, width=BAR_WIDTH)
    ])

    company_name = entry.get('name', entry.get('symbol', 'unknown'))
    source_info = entry.get('longterm_pe_source', '-')

    fig.update_layout(
        barmode='group',
       title={
            'text': f"<b>{company_name}</b><br><span style='font-size:13px; color:gray;'>Longterm PE: {source_info}</span>",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=350,
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
            'display': 'inline-block',
            'boxShadow': '0 2px 6px rgba(0,0,0,0.08)',
            'borderRadius': '10px',
            'backgroundColor': '#ffffff',
            'padding': '12px',
            'margin': '0.5%',
            'verticalAlign': 'top'
        }
    )

# dropdown options
sectors = sorted(set(d.get("sector", "unknown") for d in data if d.get("sector")))
indices = sorted(set(d.get("index", "unknown") for d in data if d.get("index")))

app.layout = html.Div([
    # heading
    html.H1(app.title, style={
        'fontFamily': 'Roboto, sans-serif',
        'textAlign': 'center',
        'padding': '20px 10px',
        'color': '#333'
    }),
    # dropdowns
    html.Div([
        html.Label("Sector", style={'marginRight': '10px'}),
        dcc.Dropdown(
            options=[{'label': 'Alle', 'value': 'ALL'}] + [{'label': s, 'value': s} for s in sectors],
            value='ALL',
            id='sector-filter',
            style={'width': '280px'}
        ),

        html.Label("Index", style={'marginLeft': '30px', 'marginRight': '30px'}),
        dcc.Dropdown(
            options=[{'label': 'Alle', 'value': 'ALL'}] + [{'label': i, 'value': i} for i in indices],
            value='ALL',
            id='index-filter',
            style={'width': '280px'}
        ),
    ], style={'fontFamily': 'Roboto, sans-serif','display': 'flex', 'alignItems': 'center', 'padding': '10px'}),

    # stock cards
    html.Div(id='chart-container', style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))',
        'gap': '35px',
        'padding': '20px'
    })
])

@app.callback(
    Output('chart-container', 'children'),
    Input('sector-filter', 'value'),
    Input('index-filter', 'value')
)
def update_cards(sector, index):
    filtered = data
    if sector != 'ALL':
        filtered = [d for d in filtered if d.get("sector") == sector]
    if index != 'ALL':
        filtered = [d for d in filtered if d.get("index") == index]

    return [create_company_card(entry) for entry in filtered]


if __name__ == '__main__':
    app.run(debug=True)
