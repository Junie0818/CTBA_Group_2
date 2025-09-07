import dash
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output
import dash

dash.register_page(__name__, path='/page1', title='Home', name='Page 1')


df = pd.read_csv("data/US_Median_Housing_Prices.csv")

fig = px.line(df, x = 'Dates', y = 'California', title = "California Housing Prices")


layout = html.Div([
    html.Div("Top (1st  Row)", className="block block-top"),

    html.Div([
        html.Div("Middle Left", className="block"),
        html.Div("Middle Right", className="block")
    ],

    className="row-2"),

   
    dcc.Graph(
        id='california-housing-graph',
        figure=fig
    ),


    html.Div(
        "Footer", className="block block-footer"
    )
],
className = "page1-grid")