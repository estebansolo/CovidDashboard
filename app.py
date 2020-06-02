import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import covid
import examples
from server import app

app.layout = html.Div([
    dcc.Tabs(
        id="tabs_manager",
        value="covid_19",
        children=[
            dcc.Tab(label="Covid 19", value="covid_19"),
            dcc.Tab(label="Examples", value="examples")
        ]
    ),
    html.Div(id='tabs_content'),
    html.Div(
        [
            html.Div("Web Dashboard using Dash framework for Python."),
            html.Div("Esteban Solorzano, 2020")
        ],
        style={
            "textAlign": "right",
            "color": "gray",
            "marginTop": "15px"
        }
    )
])

@app.callback(
    Output("tabs_content", "children"),
    [Input("tabs_manager", "value")]
)
def render_tab(tab):
    if tab == "covid_19":
        return covid.all
    
    return examples.all

if __name__ == "__main__":
    app.run_server()