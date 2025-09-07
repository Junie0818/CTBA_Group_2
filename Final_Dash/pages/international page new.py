# pages/2_international.py
# International Housing (Minimal) — two-column layout + country dropdown + line chart

import pandas as pd
import numpy as np
from datetime import datetime

import requests
import dash
from dash import Dash, html, dcc, Input, Output, callback, register_page
import plotly.express as px
from pathlib import Path
import dash_bootstrap_components as dbc

# --- Load the international data. csv from disk.
# read the CSV containing state-level median home prices with monthly columns
#dash.register_page(__name__, path='/Page2',name='Page2')
#DATA_PATH = Path(__file__).resolve().parent.parent /"data" / "international_housing_nominal.csv"
#df = pd.read_csv(DATA_PATH)


def load_international_data():
   
    try:
        # Loading international data
        df = pd.read_csv('international_housing_nominal.csv', encoding='latin1')
        df = df.dropna(subset=['price'])
        
        # Standardised time format
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['quarter'] = df['date'].dt.quarter
        
        # Standardised listings 
        df_standard = df.rename(columns={
            'country': 'region_name',
            'price': 'price_index'
        })
        df_standard['region_type'] = 'country'
        
        # Returns standardised columns
        return df_standard[['date', 'year', 'quarter', 'region_name', 'region_type', 'price_index']].copy()
        
    except Exception as e:
        print(f"Error loading international data: {e}")
        return pd.DataFrame()
    
# Pre-loaded data
df_global = load_international_data()
country_list = df_global['region_name'].unique().tolist() if not df_global.empty else []
default_country = country_list[0] if country_list else None

##app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


##layout
app.layout=html.Div(
        [
            # Left column: drop-down selection
            html.Div(
                [
                    html.H4("Select Country"),
                    dcc.Dropdown(
                        id="intl-country",
                        options=[{"label": c, "value": c} for c in  country_list],
                        value= default_country,
                        clearable=False,
                        style={"width": "100%"}
                    )
                ],
                style={"width": "30%", "display": "inline-block", "verticalAlign": "top", "padding": "8px"}
            ),

            # Right column: line graph
            html.Div(
                [
                    dcc.Graph(id="intl-line", style={"height": "70vh"})
                ],
                style={"width": "69%", "display": "inline-block", "verticalAlign": "top", "padding": "8px"}
            ),
        ],
        style={"padding": "12px"}
    )

@callback(
    Output("intl-line", "figure"),
    Input("intl-country", "value"),
    prevent_initial_call=False
)
def update_chart(selected_country):
    # empty choice processing
    if not selected_country:
        return px.line(title="Select a country to see recent housing price trends")

    # Pulling data from the country
    dff = df_global[df_global['region_name'] == selected_country].copy()

    if dff.empty:
        fig = px.line(title=f"No data for {selected_country}")
        fig.add_annotation(text=f"No data for {selected_country}", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
        return fig

    # last 10years
    dff["date"] = pd.to_datetime(dff["date"], errors="coerce")
    dff = dff.dropna(subset=["date", "price_index"]).sort_values("date")
    if not dff.empty:
        cutoff = dff["date"].max() - pd.DateOffset(years=10)
        dff = dff[dff["date"] >= cutoff]

    fig = px.line(
        dff,
        x="date",
        y="price_index",
        markers=True,
        title=f"Housing Price Trend — {selected_country} (Last 10 Years)"
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Housing Price Index", hovermode="x unified")
    fig.update_yaxes(tickformat=",.0f")
    return fig

##run serve
if __name__ == '__main__':
    app.run(debug=True)
