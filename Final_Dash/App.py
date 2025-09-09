import dash
from dash import Dash, html, Input, Output, callback, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, 
           title="Team 2 Group Dash",external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server ##for deployment



navbar = dbc.NavbarSimple(
        children=[
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("United States", href="/states", active="exact"),
            dbc.NavLink("International", href="/international", active ="exact"),
            dbc.NavLink("Salary/Housing", href="/CoL", active ="exact")
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