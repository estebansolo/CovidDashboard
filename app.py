import json
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

countries = covid['Country/Region'].unique()
dropdown_options = [{'label': country, 'value': country} for country in countries]

app.layout = app.layout = html.Div([
    html.H1("Dashboard using Dash", style={
        'textAlign': 'center',
        'color': '#333333',
        'fontFamily': "arial"
    }),
    dcc.Markdown(markdown_text),
    html.Label("Countries"),
    dcc.Dropdown(
        options=dropdown_options,
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
    html.Pre(id="events_graph_results"),
    dcc.Graph(id="covid_global_graph"),
    dcc.Graph(id="covid_pie_graph")
])

@app.callback(
    [
        Output("covid_global_graph", "figure"),
        Output("covid_pie_graph", "figure")
    ],
    [
        Input("country", "value"),
        Input(component_id="datepicker", component_property="start_date"),
        Input(component_id="datepicker", component_property="end_date")
    ]
)
def update_covid_graph(countries, start_date, end_date):
    covid_graph = covid

    if countries:
        covid_graph = covid_graph[covid_graph["Country/Region"].isin(countries)]

    covid_graph = covid_graph.groupby([covid["Date"]]).sum()
    
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        covid_graph = covid_graph[covid_graph.index >= start_date]

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        covid_graph = covid_graph[covid_graph.index <= end_date]

    dates = covid_graph.index
    confirmed = covid_graph["Confirmed"].values
    deaths = covid_graph["Deaths"].values
    recovered = covid_graph["Recovered"].values

    return (
        {
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
        },
        {
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
    )


"""
hoverData: Mouse over values in the graph
clickData: Click on points in the graph
selectedData: lasso or rectangle and then select points in the graph
relayoutData: zomm auto scale and more tools
"""
@app.callback(
    Output('events_graph_results', 'children'),
    [Input('covid_global_graph', 'clickData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

if __name__ == "__main__":
    app.run_server(debug=True)