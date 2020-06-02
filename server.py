import dash

app = dash.Dash(__name__)
app.title = "Covid 19 | Dashboard"
app.config.suppress_callback_exceptions = True

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

basic_layout = {
    'plot_bgcolor': colors['background'],
    'paper_bgcolor': colors['background'],
    'font': {
        'color': colors['text']
    }
}