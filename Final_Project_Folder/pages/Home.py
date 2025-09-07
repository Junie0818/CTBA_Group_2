import dash
from dash import Dash, html, dcc, callback, Input, Output

dash.register_page(__name__, path='/', title='Home', name='Home')

layout = html.Div([
    html.H2("Welcome to my Home Page"),
    html.P("This is a simple multi-page Dash project example."),
    
])