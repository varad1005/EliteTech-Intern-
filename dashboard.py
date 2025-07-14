import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("flights.csv")

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Flight Delay Dashboard"

app.layout = dbc.Container([
    html.H1("✈️ Flight Delay Dashboard", style={'textAlign': 'center', 'color': '#00d8ff'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            html.Label("Select Airport:", style={'color': 'white'}),
            dcc.Dropdown(
                id='airport-dropdown',
                options=[{'label': a, 'value': a} for a in df['Airport'].unique()],
                value='JFK',
                clearable=False,
                style={'color': '#000'}
            )
        ], width=6),
        dbc.Col([
            html.Div(id='flight-count', style={
                'color': '#00ffcc', 'fontSize': 20, 'marginTop': '35px', 'textAlign': 'center'
            })
        ], width=6)
    ]),

    html.Br(),

    dcc.Graph(id='delay-bar'),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.H5("✈️ Airline Distribution", style={'color': 'white'}),
            dcc.Graph(id='airline-pie')
        ], width=6),
        dbc.Col([
            html.H5("🔥 Top 3 Most Delayed Airlines", style={'color': 'white'}),
            dash_table.DataTable(
                id='top-delays-table',
                columns=[
                    {'name': 'Airline', 'id': 'Airline'},
                    {'name': 'Delay', 'id': 'Delay'}
                ],
                style_cell={'backgroundColor': '#111', 'color': '#fff', 'textAlign': 'center'},
                style_header={'backgroundColor': '#222', 'fontWeight': 'bold'}
            )
        ], width=6)
    ])

], fluid=True, style={'padding': '30px'})


# Callbacks
@app.callback(
    Output('delay-bar', 'figure'),
    Output('flight-count', 'children'),
    Output('airline-pie', 'figure'),
    Output('top-delays-table', 'data'),
    Input('airport-dropdown', 'value')
)
def update_dashboard(airport):
    dff = df[df['Airport'] == airport]

    # Bar chart
    fig_bar = px.bar(dff, x='Airline', y='Delay', color='Airline',
                     title=f"Avg Delays at {airport}", labels={'Delay': 'Delay (min)'})
    fig_bar.update_layout(template='plotly_dark')

    # Total flights
    flight_count_text = f"🛫 Total Flights at {airport}: {len(dff)}"

    # Pie chart
    pie_fig = px.pie(dff, names='Airline', title='Airline Share')
    pie_fig.update_layout(template='plotly_dark')

    # Top 3 delays
    top_3 = dff.sort_values(by='Delay', ascending=False).head(3)
    table_data = top_3[['Airline', 'Delay']].to_dict('records')

    return fig_bar, flight_count_text, pie_fig, table_data


# Run
if __name__ == '__main__':
    app.run(debug=True)







