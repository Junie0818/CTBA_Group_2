import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

#Initialize the app
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, title="Multi-Page-App")
server = app.server #For deployment


app.layout = html.Div([
    dbc.NavbarSimple(
        children = [dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page1", active="exact"),
                
                ],
        brand="Multi-Page App"),
        dash.page_container
    ])

if __name__ == '__main__':
    app.run(debug=True)