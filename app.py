import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

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
    )
])



if __name__ == "__main__":
    app.run_server(debug=True)