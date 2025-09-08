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
dash.register_page(__name__, path='/Page2',name='Page2')
# DATA_PATH = Path(__file__).resolve().parent.parent /"data" / "international_housing_nominal.csv"

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "international_housing_nominal.csv"

##data loading
def load_international_data():
    
    ##read international_housing_nominal.csv and standardised as: 
    # ['date','year','quarter','region_name','region_type','price_index']
    
    if not DATA_PATH.exists():
        err = f"[ERROR] CSV not found at: {DATA_PATH}"
        print(err)
        return pd.DataFrame(), err
    
    try:
        
        df = pd.read_csv(DATA_PATH, encoding='latin1')
        df.columns = [c.strip().lower() for c in df.columns]
           
        required = {"date", "country", "price"}
        if not required.issubset(df.columns):
            err = f"[ERROR] Missing columns. Need {required}, found {set(df.columns)}"
            print(err)
            return pd.DataFrame(), err
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date','price']).copy()

          # Reservations after 2000 only
        df = df[df["date"].dt.year >= 2000]

          
        # “Emerging market economies (aggregate)”、"Advanced economies"
        mask_agg = df["country"].str.contains("economies|aggregate", case=False, na=False)
        df = df[~mask_agg].copy()

        # rename
        df = df.rename(columns={"country": "region_name", "price": "price_index"})
        df["region_type"] = "country"
        df["year"] = df["date"].dt.year
        df["quarter"] = df["date"].dt.quarter

        out = df[["date", "year", "quarter", "region_name", "region_type", "price_index"]]\
                .sort_values(["region_name", "date"]).reset_index(drop=True)

        if out.empty:
            err = "[WARN] CSV loaded but no valid rows after cleaning (check year/price)."
            print(err)
            return pd.DataFrame(), err

        
        print("[DEBUG] Loaded rows:", len(out))
        print("[DEBUG] Sample countries:", sorted(out["region_name"].unique().tolist())[:10])
        return out, None

    except Exception as e:
        err = f"[ERROR] Error loading international data: {e}"
        print(err)
        return pd.DataFrame(), err

df_global, load_error = load_international_data()
country_list = sorted(df_global["region_name"].unique().tolist()) if not df_global.empty else []
default_country = country_list[0] if country_list else None
years_all = sorted(df_global["year"].dropna().unique().tolist()) if not df_global.empty else []
default_year = years_all[-1] if years_all else None

# ----------------------------
# Layout components
# ----------------------------
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

controls_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Controls", className="mb-3"),

            dbc.Label("Country"),   
            dcc.Dropdown(
                id="intl-country",
                options=[{"label": c, "value": c} for c in country_list],
                value=default_country,
                clearable=False,
                style={"marginBottom": "12px"}
            ),

            dbc.Label("Year (window end)"),
            dcc.Dropdown(
                id="intl-year",
                options=[{"label": str(y), "value": y} for y in years_all],
                value=default_year,
                clearable=False,
                style={"marginBottom": "12px"}
            ),

            dbc.Button("Refresh", id="refresh", n_clicks=0, color="primary", className="mt-2"),

            html.Hr(),
            html.Small("Data source: BIS Data Portal", className="text-muted"),
        ]
    ),
    className="bg-light"
)

# KPI ：latest data
kpi_latest = dbc.Card(
    dbc.CardBody([html.H6("Latest Median House Price (or Index)"),
                  html.H2(id="kpi-latest", className="mb-0")])
)

# Growth rate card: average growth rate + annualised growth rate
growth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Calculation of the average growth rate", className="mb-2"),
            html.H3(id="avg-growth", className="mb-3"),

            html.H6("Calculation of annualised growth rate", className="mb-2"),
            html.H3(id="annualised-growth", className="mb-0"),
        ]
    )
)

# Line graph cards: last 5 years
chart_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Last 5 Years - Housing Price Trend"),
            dcc.Loading(
                dcc.Graph(id="intl-line", style={"height": "60vh"}),
                type="default"
            )
        ]
    )
)

layout = dbc.Container(
    [
        html.H3("International Housing Price Dashboard", className="mt-3 mb-3"),
        dbc.Row(
            [
                dbc.Col(controls_card, width=3),
                dbc.Col(
                    [
                        kpi_latest,
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(growth_card, md=6),
                                dbc.Col(chart_card, md=6),
                            ],
                            className="gy-3"
                        ),
                    ],
                    width=9
                ),
            ],
            className="g-3"
        )
    ],
    fluid=True
)

# ----------------------------
# calculate function
# ----------------------------
def compute_window(df_country: pd.DataFrame, end_year: int, window_years: int = 5) -> pd.DataFrame:
    """return [end_year - window_years + 1, end_year] time window data, if insufficient, is automatically truncated."""
    if df_country.empty or pd.isna(end_year):
        return df_country.iloc[0:0]

    # time scope
    min_year = int(df_country['year'].min())
    max_year = int(df_country['year'].max())

    end_y = min(int(end_year), max_year)
    start_y = max(min_year, end_y - (window_years - 1))

    win = df_country[(df_country['year'] >= start_y) & (df_country['year'] <= end_y)].copy()
    return win.sort_values('date')

def fmt_money_or_index(x):
    if pd.isna(x):
        return "—"
    # $
    return f"${x:,.2f}"

def avg_qoq_growth_pct(window_df: pd.DataFrame):
    
    if len(window_df) < 2:
        return None
    s = window_df['price_index'].astype(float)
    qoq = s.pct_change().dropna()
    if qoq.empty:
        return None
    return float(qoq.mean() * 100.0)  # Average growth per quarter (%)

def annualised_cagr_pct(window_df: pd.DataFrame):
   
    if len(window_df) < 2:
        return None
    s = window_df['price_index'].astype(float)
    start = float(s.iloc[0])
    end = float(s.iloc[-1])
    # Quarterly cycle
    quarters = len(window_df) - 1
    if start <= 0 or quarters <= 0:
        return None
    cagr = (end / start) ** (4.0 / quarters) - 1.0
    return float(cagr * 100.0)

# ----------------------------
# Pullback: update KPIs / growth rates / line charts
# ----------------------------
@callback(
    Output("kpi-latest", "children"),
    Output("avg-growth", "children"),
    Output("annualised-growth", "children"),
    Output("intl-line", "figure"),
    Input("intl-country", "value"),
    Input("intl-year", "value"),
    Input("refresh", "n_clicks")
)
def update_dashboard(country, end_year, _n_clicks):
    # error
    if not country or df_global.empty:
        fig = px.line(title="No data")
        return "—", "—", "—", fig

    # National quantitative data (for KPI updates)
    dff_full = df_global[df_global['region_name'] == country].copy()
    if dff_full.empty:
        fig = px.line(title=f"No data for {country}")
        return "—", "—", "—", fig

    # KPI：
    latest_row = dff_full.sort_values('date').iloc[-1]
    latest_val = latest_row['price_index']
    latest_text = fmt_money_or_index(latest_val)

    # latest 5 year
    win = compute_window(dff_full, end_year, window_years=5)

    # average growth
    avg_pct = avg_qoq_growth_pct(win)
    cagr_pct = annualised_cagr_pct(win)
    avg_txt = f"{avg_pct:+.2f}%" if avg_pct is not None else "N/A"
    cagr_txt = f"{cagr_pct:+.2f}%" if cagr_pct is not None else "N/A"

    # line chart
    if win.empty:
        fig = px.line(title=f"No data window for {country} with end year {end_year}")
    else:
        start_y, end_y = int(win['year'].min()), int(win['year'].max())
        fig = px.line(
            win, x="date", y="price_index",
            markers=True,
            title=f"{country} – {start_y} to {end_y}"
        )
        fig.update_layout(
            xaxis_title="Date", yaxis_title="Housing Price",
            hovermode="x unified", margin=dict(l=10, r=10, t=60, b=10), height=500
        )
        # $ and Thousandths
        fig.update_yaxes(tickprefix="$", separatethousands=True)

    return latest_text, avg_txt, cagr_txt, fig



##run serve
# if __name__ == '__main__':
#     app.run(debug=True)
