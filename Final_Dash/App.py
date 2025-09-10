##AI Usage Block:
#ChatGPT was the main AI used, with some assistance recieved from CoPilot.
#AI was used to assist with designing certain functions, and to provide guidance on writing edge cases.
#AI was used to as a learning aid, providing information on good design layouts, as well as how certain functions/methods worked.
#AI was used to assist with diagnosing errors with code (only after the group spent some time trying to figure it out on their own).
#AI was also used to help deploy dashboard on render, specifically in providing insight into why code would not deploy.
#A more in-depth breakdown of our AI usage can be found in AI_Usage_Apendix.txt


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
    brand="VRJC Realty",
    brand_style={"fontSize": "35px"},
    style={'background-color': "#87A111"},
    # dark=True,
    className="mb2",
    
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid = True)



if __name__ == "__main__":
    app.run(debug=True)
