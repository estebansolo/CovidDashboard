import time
import random

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app, basic_layout
from file_manager import FileManager

covid_df = FileManager("covid_19.csv")
last_day_covid = covid_df.get_last_information()

markdown_text = """
# Some Basic Components from Dash

This tab contains some components from the Dash library used as exercises while I was learning.

[Dash Gallery](https://dash-gallery.plotly.host/Portal/)
"""

random_graph = html.Div([
    html.H1("Using Intervals to Update this Random Graph"),
    html.Div([
        html.Div([
            html.Label("Reload Interval"),
            dcc.RadioItems(
                options=[
                    {'label': '10 seconds', 'value': 10},
                    {'label': '30 seconds', 'value': 30},
                    {'label': '1 minute', 'value': 60}
                ],
                value=30,
                id="interval_options",
            ),
        ], id="options_interval"),
        dcc.Loading(id="random_loading", children=[
            html.Div(
                dcc.Graph(id="random_graph")
            )
        ], type="default"),
    ], className="graph_containers"),
    dcc.Interval(id='interval_component', interval=5000, n_intervals=0)
])

multiple_output = html.Div([
    html.H1("Multiple Outputs"),
    html.Div([
        dcc.Input(id='my-id', value="", type='text'),
    ]),
    html.Div([
        html.Div(id='my-div', className="multiple_outputs"),
        html.Div(id='my-div-reverse', className="multiple_outputs"),
    ], id="multiple_output_containers")
], style={"textAlign": "center"})

graph_event = html.Div([
    html.H1("Graph Dropdown Event"),
    html.Div([
        html.Div([
            html.Label("Countries"),
            dcc.Dropdown(
                id="country",
                value='Colombia',
                options=covid_df.countries(),
                placeholder="Select a country"
            ),
        ], id="options_country"),
        dcc.Graph(id="country_graph"),
    ], className="graph_containers"),
])


@app.callback(
    [
        Output(component_id='my-div', component_property='children'),
        Output(component_id='my-div-reverse', component_property='children')
    ],
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return (
        f'Entered: {input_value}',
        f'Reversed: {input_value[::-1]}'
    )

@app.callback(
    Output(component_id="country_graph", component_property="figure"),
    [Input(component_id="country", component_property="value")]
)
def update_graph_country(input_value):
    country = last_day_covid[last_day_covid["Country/Region"] == input_value]

    data = {
        'Confirmed': int(country['Confirmed']),
        'Deaths': int(country['Deaths']),
        'Recovered': int(country['Recovered']),
    }

    return {
        'data': [
            {'x': list(data.keys()), 'y': list(data.values()), 'type': 'bar'},
        ],
        'layout': {
            **basic_layout,
            'title': 'Covid 19',
            "yaxis": {'title': 'Cases'},
        }
    }


@app.callback(
    Output(component_id='random_graph', component_property='figure'),
    [Input(component_id='interval_component', component_property='n_intervals')]
)
def update_random_graph(input_value):
    time.sleep(1)

    countries = {
        "Colombia": random.randint(0, 100),
        "España": random.randint(0, 100),
        "Canada": random.randint(0, 100),
        "Estados Unidos": random.randint(0, 100),
        "Ecuador": random.randint(0, 100),
    }

    return {
        'data': [
            {'x': list(countries.keys()), 'y': list(countries.values()), 'type': 'linear'},
        ],
        'layout': basic_layout
    }

@app.callback(
    Output("interval_component", "interval"),
    [Input("interval_options", "value")]
)
def update_interval(interval_value):
    return interval_value * 1000

all = html.Div([
    dcc.Markdown(markdown_text, className="markdown_content"),
    html.Hr(),
    random_graph,
    html.Hr(),
    multiple_output,
    html.Hr(),
    graph_event
])