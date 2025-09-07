import dash
from dash import Dash, html, Input, Output, callback, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, 
           title="Team 2 Group Dash",external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server ##for deployment



navbar = dbc.NavbarSimple(
        children=[
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Page 1", href="/page1", active="exact"),
            dbc.NavLink("Page 2", href="/page2", active ="exact")
    ],
    brand="Team 2 Group Dash",
    color= "dark",
    dark=True,
    className="mb2",
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid = True)



if __name__ == "__main__":
    app.run(debug=True)