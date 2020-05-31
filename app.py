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

app.layout = app.layout = html.Div([
    html.H1("Dashboard using Dash", style={
        'textAlign': 'center',
        'color': '#333333',
        'fontFamily': "arial"
    }),
    dcc.Markdown(markdown_text),
])



if __name__ == "__main__":
    app.run_server(debug=True)