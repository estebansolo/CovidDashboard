from datetime import datetime

import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app, basic_layout
from file_manager import FileManager

covid_df = FileManager("covid_19.csv")
complete_covid_df = covid_df.get_covid_df()
last_data_covid = covid_df.get_last_information()


top_ten_deaths = last_data_covid.sort_values(by="Deaths").tail(10)
top_ten_confirmed = last_data_covid.sort_values(by="Confirmed").tail(10)
top_ten_recovered = last_data_covid.sort_values(by="Recovered").tail(10)

markdown_text = """
# Covid 19 Overview

Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.

This is for learning purpose using Dash library
"""

overview = html.Div([
    html.Div([
        html.Label("Countries"),
        dcc.Dropdown(
            options=covid_df.countries(),
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
    ], id="overview_options"),
    html.Div([
        dcc.Loading(dcc.Graph(id="covid_global_graph")),
        dcc.Loading(dcc.Graph(id="covid_pie_graph")),
    ], id="overview_graphs")
], id="overview_container")

top_ten = html.Div([
    html.H1("Top 10 Countries"),
    html.Div([
        dcc.Graph(
            id="covid_ten_confirmed",
            figure={
                'data': [
                    go.Bar(
                        y=top_ten_confirmed["Country/Region"],
                        x=top_ten_confirmed["Confirmed"],
                        orientation='h',
                        texttemplate="%{x:.2s}",
                        textposition='auto'
                    )
                ],
                "layout": {
                    "title": "Confirmed",
                    "xaxis": {"showticklabels": False},
                }
            },
        ),
        dcc.Graph(
            id="covid_ten_deaths",
            figure={
                'data': [
                    go.Bar(
                        y=top_ten_deaths["Country/Region"],
                        x=top_ten_deaths["Deaths"],
                        orientation='h',
                        texttemplate="%{x:.2s}",
                        textposition='auto',
                        marker_color='lightcoral'
                    )
                ],
                "layout": {
                    "title": "Deaths",
                    "xaxis": {"showticklabels": False},
                }
            }
        ),
        dcc.Graph(
            id="covid_ten_recovered",
            figure={
                'data': [
                    go.Bar(
                        y=top_ten_recovered["Country/Region"],
                        x=top_ten_recovered["Recovered"],
                        orientation='h',
                        texttemplate="%{x:.2s}",
                        textposition='auto',
                        marker_color='forestgreen'
                    )
                ],
                "layout": {
                    "title": "Recovered",
                    "xaxis": {"showticklabels": False},
                }
            }
        ),
    ], id="top_ten_graphs")
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
    covid_overview = complete_covid_df

    if countries:
        mask_countries = covid_overview["Country/Region"].isin(countries)
        covid_overview = covid_overview[mask_countries]

    covid_overview = covid_overview.groupby([complete_covid_df["Date"]]).sum()
    
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        covid_overview = covid_overview[covid_overview.index >= start_date]

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        covid_overview = covid_overview[covid_overview.index <= end_date]

    confirmed = covid_overview["Confirmed"].values
    deaths = covid_overview["Deaths"].values
    recovered = covid_overview["Recovered"].values

    return (
        {
            'data': [
                {'x': covid_overview.index, 'y': confirmed, 'type': 'linear', 'name': 'Confirmed'},
                {'x': covid_overview.index, 'y': deaths, 'type': 'linear', 'name': 'Deaths'},
                {'x': covid_overview.index, 'y': recovered, 'type': 'linear', 'name': 'Recovered'},
            ],
            'layout': {
                **basic_layout,
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
    [
        Output('events_graph_results', 'children'),
        Output("title_event_result", "children")
    ],
    [
        Input('covid_global_graph', 'clickData'),
        Input("country", "value")
    ]
)
def display_hover_data(click_data, countries):
    covid_graph = complete_covid_df

    if click_data:
        selected_date = click_data["points"][0]["x"]
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d")
        covid_graph = covid_graph[covid_graph["Date"] == selected_date]
    else:
        dates = covid_graph["Date"].values
        covid_graph = covid_graph[covid_graph["Date"] == dates[-1]]
    
    if countries:
        covid_graph = covid_graph[covid_graph["Country/Region"].isin(countries)]

    actual_date = covid_graph["Date"].iloc[0].strftime("%b %d, %Y")
    covid_graph = covid_graph.groupby([covid_graph["Country/Region"]]).sum()
    
    country = covid_graph.index
    deaths = covid_graph["Deaths"].values
    confirmed = covid_graph["Confirmed"].values
    recovered = covid_graph["Recovered"].values

    return (
        [
            dcc.Graph(figure={
                'data': [
                    {'x': country, 'y': confirmed, 'type': 'bar', "name": "Confirmed"},
                    {'x': country, 'y': deaths, 'type': 'bar', "name": "Deaths"},
                    {'x': country, 'y': recovered, 'type': 'bar', "name": "Recovered"},
                ],
                'layout': {
                    **basic_layout,
                    "barmode": 'stack',
                    'title': 'Covid 19',
                    "yaxis": {'title': 'Cases'},
                }
            })
        ],
        f"Date: {actual_date}"
    )

all = html.Div([
    dcc.Markdown(markdown_text, className="markdown_content"),
    overview,
    html.Hr(),
    html.H1("", id="title_event_result"),
    html.P("Click in a different day to see the statistics", id="msg_statistics"),
    html.Div(id="events_graph_results"),
    html.Hr(),
    top_ten
])