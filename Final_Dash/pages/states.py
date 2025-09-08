# import requests
# import pandas as pd
# from dash import Dash, html, dcc, callback, Output, Input, register_page
# import dash
# import plotly.express as px
# from pathlib import Path
# import dash_bootstrap_components as dbc
# #both bewlow help with calendra 
# import calendar
# from collections import defaultdict

# # --- Load the Zillow state CSV from disk.
# # read the CSV containing state-level median home prices with monthly columns
# dash.register_page(__name__, path='/states',name='states')
# #DATA_PATH = Path(__file__).resolve().parent.parent /"data" / "US_median_house_state.csv"
# #df = pd.read_csv(DATA_PATH)








# # Original Code from Cade
# # turn all monthly columns to numeric values
# df = pd.read_csv("data/US_Median_Housing_Prices.csv")
# date_cols = df.columns[5:]

# df[date_cols] = df[date_cols].apply(pd.to_numeric, errors="coerce")

# #----- Making the Month and years available -----
# # month/year selection limited to your data range.
# date_index = pd.to_datetime(date_cols, errors="coerce")
# #loop to look through csv
# ym_to_col = {}
# for d, col in zip(date_index, date_cols):
#     if pd.notna(d):
#         key = (d.year, d.month)
#         ym_to_col[key] = col

# # create a sorted list choicef or dropdown
# years = sorted({d.year for d in date_index if pd.notna(d)})
# # sorted months 
# year_to_months = defaultdict(set)
# # accumulate all months per year with a number for that year(1,2,3...)
# for d in date_index.dropna():
#     year_to_months[d.year].add(d.month)
# # year's month set into a sorted list for clean dropdown options
# for y in list(year_to_months.keys()):
#     year_to_months[y] = sorted(year_to_months[y])

# # compute the most recent available month in the dataset for defaults
# latest_dt = max(d for d in date_index if pd.notna(d))
# # store default year from the latest timestamp
# default_year = latest_dt.year
# # store default month from the latest timestamp
# default_month = latest_dt.month

# # --- States for dropdown.---------
# # build a sorted list of state names from the RegionName column
# states = sorted(df["RegionName"].dropna().unique())

# # ---------- App ----------
# # create the Dash app and include Bootstrap CSS for styling
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # --- Top bar.
# # define a simple top navigation bar with a title and subtitle
# navbar = html.Div(
#     [
#         # main heading text
#         html.H2("US States Median House Price", className="state-main-header"),
#     ],
#     # little style before we change it in the style css
#     className="navbar navbar-light bg-white mb-4 px-3 justify-content-between align-items-center",
# )

# # --- Controls (state dropdown + month/year dropdowns)-------

# # build a controls card containing the state and month/year selection widgets
# controls = dbc.Card(
#     [
#         # card header text
#         dbc.CardHeader("Controls"),
#         # card body containing interactive inputs
#         dbc.CardBody(
#             [
#                 # label above the state dropdown
#                 dbc.Label("State"),
#                 # dropdown of all states (RegionName) with a default of CA if present
#                 dcc.Dropdown(
#                     id="state-dropdown",
#                     options=[{"label": s, "value": s} for s in states],
#                     value="Virginia" if "Virginia" in states else states[0],
#                     clearable=False,
#                 ),
#                 # label above the year dropdown
#                 dbc.Label("Year"),
#                 # dropdown for year
#                 dcc.Dropdown(
#                     id="year-dropdown",
#                     options=[{"label": str(y), "value": y} for y in years],
#                     value=default_year,
#                     clearable=False,
#                 ),
#                 # label above the month dropdown
#                 dbc.Label("Month"),
#                 # dropdown for month
#                 dcc.Dropdown(
#                     id="month-dropdown",
#                     options=[{"label": calendar.month_name[m], "value": m} for m in year_to_months[default_year]],
#                     value=default_month,
#                     clearable=False,
#                 ),
#                 # a little spacing before the refresh button
#                 html.Br(),
#                 # refresh button 
#                 dbc.Button("Refresh", id="refresh", n_clicks=0,),
#                 # horizontal break to separate controls 
#                 html.Hr(),
#                 # small text showing the data source
#                 html.Small("Data source: Zillow.com."),
#             ]
#         ),
#     ],
#     # spacing class to separate the controls card from other elements
#     className="state-dropdown-controls", 
# )

# # --- KPI card that shows the latest value--------
# def price_card(id_):
#     return dbc.Card(
#         dbc.CardBody(
#             [
#                 html.H6("Latest Mean House Price"),
#                 html.H2(id=id_),
#             ]
#         ),
#         className="state-latest-price",
#     )
# # a row at the top of the right column to show the KPI card
# kpi_row = dbc.Row(
#     [
#         dbc.Col(price_card("kpi-median-price")),
#     ])

# #shows the exact value for the selected year/month for the chosen state
# bottom_readout = dbc.Card(
#     dbc.CardBody([
#         html.H6("Selected Month Value"),
#         html.Div(id="selected-month-value"),
#     ])
# )

# # --- Percent change & IRR 
# # card shows percent change from selected month to the latest
# percent_change_card = dbc.Card(
#     dbc.CardBody([
#         html.H6("Percent Change (Selected → Current)"),
#         html.Div(id="pct-change"),
#         html.Hr(),
#         html.H6("IRR (Selected → Current)"),
#         html.Div(id="irr-text"),
#     ])
# )

# #line chart to visualize price change
# trend_line_card = dbc.Card(
#     dbc.CardBody([
#         html.H6("Price Trend (Selected → Current)"),
#         dcc.Graph(id="pct-line"),
#     ])
# )

# # --- Layout------
# app.layout = dbc.Container(
#     [
#         navbar,
#         dbc.Row(
#             [
#                 dbc.Col(controls, width=2),
#                 dbc.Col(trend_line_card, width = 7),
#                 dbc.Col(
#                     [
#                         kpi_row,
#                         dbc.Row(
#                             [
#                                 dbc.Col(bottom_readout),
#                                 dbc.Col(percent_change_card),
#                             ],),
#                     ],
#                 ),
#             ],
#         ),
#     ],
#     fluid=True,
# )

# # ---------- Callbacks ----------

# # --- only show months that exist in your data for that year
# @callback(
#     Output("month-dropdown", "options"), 
#     Output("month-dropdown", "value"),   
#     Input("year-dropdown", "value"),    
# )
# def sync_month_options(selected_year):
#     months = year_to_months.get(selected_year, [])
#     options = [{"label": calendar.month_name[m], "value": m} for m in months]
#     value = months[-1] if months else None
#     return options, value

# # --- Update the KPI (latest value),  the % change, the IRR, and the line figure.
# @callback(
#     Output("kpi-median-price", "children"), 
#     Output("selected-month-value", "children"),  
#     Output("pct-change", "children"),  
#     Output("irr-text", "children"),  
#     Output("pct-line", "figure"), 
#     Input("state-dropdown", "value"), 
#     Input("year-dropdown", "value"), 
#     Input("month-dropdown", "value"),  
#     Input("refresh", "n_clicks"), 
# )
# def update_kpi(selected_state, sel_year, sel_month, _):
#     row = df.loc[df["RegionName"] == selected_state]
#     latest_col = date_cols[-1]
#     latest_val = row[latest_col].iloc[0]
#     kpi_text = f"${latest_val:,.0f}" if pd.notna(latest_val) else "—"

#     if not sel_year or not sel_month:
#         return kpi_text, "Select a year and month", "Select a year and month", "Select a year and month", px.line()

#     col = ym_to_col.get((int(sel_year), int(sel_month)))
#     #missing data
    
#     sel_val = row[col].iloc[0]
#     # missing data
#     if pd.isna(sel_val):
#         month_text = "—"
#         pct_text = "—"
#         irr_text = "—"
#         return kpi_text, month_text, pct_text, irr_text, px.line()

#     month_text = f"{selected_state} — {calendar.month_name[int(sel_month)]} {sel_year}: ${sel_val:,.0f}"

#     # % change
#     if sel_val == 0 or pd.isna(latest_val):
#         pct_text = f"{selected_state}: N/A (insufficient data)"
#     else:
#         pct = (latest_val - sel_val) / sel_val * 100.0
#         pct_text = f"{selected_state}: {pct:+.2f}%"

#     # compute IRR 
#     months_diff = (latest_dt.year - int(sel_year)) * 12 + (latest_dt.month - int(sel_month))
 
#     if months_diff <= 0 or sel_val <= 0 or pd.isna(latest_val):
#         irr_text = f"{selected_state}: IRR N/A"
#     else:
#         annualized_irr = (latest_val / sel_val) ** (12.0 / months_diff) - 1.0
#         irr_text = f"{selected_state}: {annualized_irr*100:.2f}% annualized"

#     # build a small time series from the selected month up to the latest month to plot
#     ts_all = pd.Series(row[date_cols].iloc[0].values, index=date_index)
#     # determine the datetime corresponding exactly date so we say day 1
#     start_dt = pd.Timestamp(year=int(sel_year), month=int(sel_month), day=1)
#     # find the timestamp in the index with the same year/month (CSV headings are end-of-month)
#     matches = [d for d in date_index if (pd.notna(d) and d.year == int(sel_year) and d.month == int(sel_month))]
#     # selected timestamp through the latest data point
#     ts_window = ts_all[(ts_all.index >= start_dt) & (ts_all.index <= latest_dt)]

#     fig = px.line(
#         x=ts_window.index,     
#         y=ts_window.values,    
#         labels={"x": "Date", "y": "Median house Price ($)"},  
#         title=None,            
#         )
#         # tighten margins and set a compact height to fit next to the card
#     fig.update_layout(margin=dict(t=20, r=20, b=20, l=20), height=480, hovermode="x unified")
#     fig.update_yaxes(tickprefix="$", separatethousands=True)

#     # return all 
#     return kpi_text, month_text, pct_text, irr_text, fig

# # --- Run it
# if __name__ == "__main__":
#     app.run(debug=True)
