import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

markdown_text = """
# Dashboard using Dash

- Flask
- Plotly.js
- React.js

[Dash Gallery](https://dash-gallery.plotly.host/Portal/)
"""

app.layout = dcc.Markdown(markdown_text)

if __name__ == "__main__":
    app.run_server(debug=True)