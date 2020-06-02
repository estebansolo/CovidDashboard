import json
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd

app = dash.Dash(__name__)

app.title = "Covid 19 | Dashboard"

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
    dcc.Graph(id="covid_global_graph"),
    dcc.Graph(id="covid_pie_graph"),
    html.Div(id="events_graph_results"),
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
    [
        Input('covid_global_graph', 'clickData'),
        Input("country", "value")
    ]
)
def display_hover_data(click_data, countries):
    if not click_data:
        return html.Div("Please select a day in the Graph.")
    
    covid_graph = covid
    selected_date = click_data["points"][0]["x"]

    selected_date = datetime.strptime(selected_date, "%Y-%m-%d")
    covid_graph = covid_graph[covid_graph["Date"] == selected_date]

    if countries:
        covid_graph = covid_graph[covid_graph["Country/Region"].isin(countries)]

    covid_graph = covid_graph.groupby([covid_graph["Country/Region"]]).sum()
    
    country = covid_graph.index
    confirmed = covid_graph["Confirmed"].values
    deaths = covid_graph["Deaths"].values
    recovered = covid_graph["Recovered"].values

    return [
        dcc.Graph(figure={
            'data': [
                {'x': country, 'y': confirmed, 'type': 'bar', "name": "Confirmed"},
                {'x': country, 'y': deaths, 'type': 'bar', "name": "Deaths"},
                {'x': country, 'y': recovered, 'type': 'bar', "name": "Recovered"},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                "barmode": 'stack',
                'title': 'Covid 19',
                "yaxis": {'title': 'Cases'},
            }
        })
    ]


if __name__ == "__main__":
    app.run_server(debug=True)