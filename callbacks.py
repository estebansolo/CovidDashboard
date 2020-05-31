import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

covid = pd.read_csv("covid_19.csv")

covid["Date"] = pd.to_datetime(covid["Date"])
covid_by_date = covid.groupby([covid["Date"], covid["Country/Region"]]).sum()
covid_by_date.reset_index(level=['Country/Region'], inplace=True)

covid_last = covid_by_date[covid_by_date.index == covid_by_date.index[-1]]

countries = covid['Country/Region'].unique()
dropdown_options = [{'label': country, 'value': country} for country in countries]

app.layout = app.layout = html.Div([
    dcc.Input(id='my-id', value="", type='text'),
    html.Div(id='my-div'),
    html.Div(id='my-div-reverse'),
    html.Label("Countries"),
    dcc.Dropdown(
        id="country",
        options=dropdown_options,
        value='Colombia',
        placeholder="Select a country"
    ),
    dcc.Graph(id="country_graph", animate=True),
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
        'You\'ve entered "{}"'.format(input_value),
        input_value[::-1]
    )

@app.callback(
    Output(component_id="country_graph", component_property="figure"),
    [Input(component_id="country", component_property="value")]
)
def update_graph_country(input_value):
    country = covid_last[covid_last["Country/Region"] == input_value]

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
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            },
            'title': 'Covid 19',
            "yaxis": {'title': 'Cases'},
        }
    }

if __name__ == "__main__":
    app.run_server(debug=True)