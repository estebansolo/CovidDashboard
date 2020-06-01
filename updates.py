import dash
import random
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

VALID_USERNAME_PASSWORDS = {
    'hello': 'world'
}

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORDS)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = app.layout = html.Div([
    html.Label("Interval"),
    dcc.RadioItems(
        options=[
            {'label': '1 second', 'value': 1},
            {'label': '5 seconds', 'value': 5},
            {'label': '10 seconds', 'value': 10}
        ],
        value=1,
        id="interval_options",
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="random_graph"),
    dcc.Interval(id='interval_component', interval=1000, n_intervals=0)
])

@app.callback(
    Output(component_id='random_graph', component_property='figure'),
    [Input(component_id='interval_component', component_property='n_intervals')]
)
def update_graph(input_value):
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
        'layout': {
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            },
            'title': 'Covid 19',
        }
    }

@app.callback(
    Output(component_id="interval_component", component_property="interval"),
    [Input(component_id="interval_options", component_property="value")]
)
def update_interval(interval_value):
    return interval_value * 1000

if __name__ == "__main__":
    app.run_server(debug=True)