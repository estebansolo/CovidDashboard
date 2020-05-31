import dash
import dash_core_components as dcc
import dash_html_components as html

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
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'Basic Data Visualization',
                "xaxis": {'title': 'X Axis'},
                "yaxis": {'title': 'Y Axis'},
            }
        }
    )
])



if __name__ == "__main__":
    app.run_server(debug=True)