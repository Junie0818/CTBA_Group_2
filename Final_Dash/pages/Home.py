import dash
from dash import html

dash.register_page(__name__, path="/", name="Home")


layout = html.Div(
    style={"margin": "0", "backgroundColor": "#99A49F"},
    children=[
        html.H1("Welcome to Team 2`s Dashboard",
                style={"margin":"0","backgroundColor": "#293831", "padding": "40px","color":"#CDD6D3", "textAlign": "center", "font-size":"35px"}),
        html.P("If you are looking for a change in scenary you`ve come to the right place. Choose your new home state based on our available median housing price date. Or broaden your horizons and find an international location by comparing prices in various cities in China.",
               style={"font-size":"20px","margin":"0","backgroundColor": "#99A49F", "padding": "20px","color": "#101513", "textAlign": "center"}),
        html.Br(),
        html.P("We hope you enjoy our comprehensive list of both American and Chinese median housing prices.", style={"textAlign": "center", "padding": "40px", "font-size":"20px"})
   
    ])

