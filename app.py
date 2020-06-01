from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd

app = dash.Dash(__name__)

markdown_text = """
- Flask
- Plotly.js
- React.js

[Dash Gallery](https://dash-gallery.plotly.host/Portal/)
"""

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

covid = pd.read_csv("covid_19.csv")
covid["Date"] = pd.to_datetime(covid["Date"])
covid_by_date = covid.groupby([covid["Date"]]).sum()

dates = covid_by_date.index
confirmed = covid_by_date["Confirmed"].values
deaths = covid_by_date["Deaths"].values
recovered = covid_by_date["Recovered"].values

app.layout = app.layout = html.Div([
    html.H1("Dashboard using Dash", style={
        'textAlign': 'center',
        'color': '#333333',
        'fontFamily': "arial"
    }),
    dcc.Markdown(markdown_text),
    html.Label("Countries"),
    dcc.Dropdown(
        options=[
            {'label': 'Colombia', 'value': 'Colombia'},
            {'label': 'Estados Unidos', 'value': 'Estados Unidos'},
            {'label': 'España', 'value': 'España'}
        ],
        multi=True,
        id="country",
        placeholder="Select a country"
    ),
    html.Label('Dates Range'),
    dcc.DatePickerRange(
        id="datepicker",
        min_date_allowed=datetime(2020, 1, 20),
        max_date_allowed=datetime(2020, 5, 25),
        display_format='MMM Do, YY',
        minimum_nights=3,
        clearable=True
    ),
    dcc.Graph(
        figure={
            'data': [
                {'x': dates, 'y': confirmed, 'type': 'linear', 'name': 'Confirmed'},
                {'x': dates, 'y': deaths, 'type': 'linear', 'name': 'Deaths'},
                {'x': dates, 'y': recovered, 'type': 'linear', 'name': 'Recovered'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'Covid 19',
                "xaxis": {'title': 'Date'},
                "yaxis": {'title': 'Cases'},
            }
        }
    ),
    dcc.Graph(
        figure={
            "data": [
                go.Pie(
                    labels=['Actives', 'Deaths', 'Recovered'],
                    values=[(confirmed[-1] - deaths[-1] - recovered[-1]), deaths[-1], recovered[-1]]
                )
            ],
            "layout": {
                "title": 'Cases Percentage'
            }
        }
    ),
    html.Div(id="hidden_value")
])

@app.callback(
    Output("hidden_value", "children"),
    [
        Input("country", "value"),
        Input(component_id="datepicker", component_property="start_date"),
        Input(component_id="datepicker", component_property="end_date")
    ]
)
def update_covid_graph(countries, start_date, end_date):
    print(countries)
    print(start_date, end_date)
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)