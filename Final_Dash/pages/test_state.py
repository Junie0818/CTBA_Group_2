# # import requests
# # import pandas as pd
# # from dash import Dash, html, dcc, callback, Output, Input, register_page
# # import dash
# # import plotly.express as px
# # from pathlib import Path
# # import dash_bootstrap_components as dbc
# # #both bewlow help with calendra 
# # import calendar
# # from collections import defaultdict
# # import numpy as np
# # from statsmodels.tsa.arima.model import ARIMA

# # # --- Load the Zillow state CSV from disk.
# # # read the CSV containing state-level median home prices with monthly columns

# # dash.register_page(__name__, path='/states',name='States')

# # #DATA_PATH = Path(__file__).resolve().parent.parent /"data" / "US_median_house_state.csv"
# # #df = pd.read_csv(DATA_PATH)


# # # turn all monthly columns to numeric values
# # df = pd.read_csv("data/US_Median_Housing_Prices.csv", header=0, index_col=0)


# # # df[date_cols] = df[date_cols].apply(pd.to_numeric, errors="coerce")
# # # df.index = pd.to_numeric(df.index, errors="coerce")

# # #----- Making the Month and years available -----
# # # month/year selection limited to your data range.
# # df.index = pd.to_datetime(df.index, format="%m/%d/%Y", errors="coerce")
# # date_index = df.index
# # # date_index = pd.to_datetime(df.index, format="%m/%d/%Y", errors="coerce")

# # #loop to look through csv
# # ym_to_col = {}
# # for d in date_index.dropna():
# #     key = (d.year, d.month)
# #     ym_to_col[key] = d

# # # create a sorted list choicef or dropdown
# # years = sorted({d.year for d in date_index if pd.notna(d)})
# # # sorted months 
# # year_to_months = defaultdict(set)
# # # accumulate all months per year with a number for that year(1,2,3...)
# # for d in date_index.dropna():
# #     year_to_months[d.year].add(d.month)
# # # year's month set into a sorted list for clean dropdown options
# # for y in list(year_to_months.keys()):
# #     year_to_months[y] = sorted(year_to_months[y])



# # # compute the most recent available month in the dataset for defaults
# # latest_dt = max(d for d in date_index if pd.notna(d))
# # # store default year from the latest timestamp
# # default_year = latest_dt.year
# # # store default month from the latest timestamp
# # default_month = latest_dt.month

# # # --- States for dropdown.---------
# # # build a sorted list of state names from the RegionName column
# # states = sorted(df.columns)

# # # ---------- App ----------
# # # create the Dash app and include Bootstrap CSS for styling
# # # app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # # --- Top bar.
# # # define a simple top navigation bar with a title and subtitle
# # navbar = html.Div(
# #     [
# #         # main heading text
# #         html.H2("US States Median House Price", className="state-main-header"),
# #         # subheading text
# #         html.Span("Public API", className="state-sub-header"),
# #     ],
# #     # little style before we change it in the style css
# #     className="navbar navbar-light bg-white mb-4 px-3 justify-content-between align-items-center",
# # )

# # # --- Controls (state dropdown + month/year dropdowns)-------
# # # build a controls card containing the state and month/year selection widgets
# # controls = dbc.Card(
# #     [
# #         # card header text
# #         dbc.CardHeader("Controls"),
# #         # card body containing interactive inputs
# #         dbc.CardBody(
# #             [
# #                 # label above the state dropdown
# #                 dbc.Label("State"),
# #                 # dropdown of all states (RegionName) with a default of CA if present
# #                 dcc.Dropdown(
# #                     id="state-dropdown",
# #                     options=[{"label": s, "value": s} for s in states],
# #                     value="Virginia" if "Virginia" in states else states[0],
# #                     clearable=False,
# #                 ),
# #                 # label above the year dropdown
# #                 dbc.Label("Year"),
# #                 # dropdown for year
# #                 dcc.Dropdown(
# #                     id="year-dropdown",
# #                     options=[{"label": str(y), "value": y} for y in years],
# #                     value=default_year,
# #                     clearable=False,
# #                 ),
# #                 # label above the month dropdown
# #                 dbc.Label("Month"),
# #                 # dropdown for month
# #                 dcc.Dropdown(
# #                     id="month-dropdown",
# #                     options=[{"label": calendar.month_name[m], "value": m} for m in year_to_months[default_year]],
# #                     value=default_month,
# #                     clearable=False,
# #                 ),
# #                 # a little spacing before the refresh button
# #                 html.Br(),
# #                 # refresh button 
# #                 dbc.Button("Refresh", id="refresh", n_clicks=0,),
# #                 # horizontal break to separate controls 
# #                 html.Hr(),
# #                 # small text showing the data source
# #                 html.Small("Data source: Zillow.com."),
# #             ]
# #         ),
# #     ],
# #     # spacing class to separate the controls card from other elements
# #     className="state-dropdown-controls",
# # )

# # # --- KPI card that shows the latest value--------
# # def price_card(id_):
# #     # create a Bootstrap card
# #     return dbc.Card(
# #         # card body contains the texts
# #         dbc.CardBody(
# #             [
# #                 html.H6("Latest Mean House Price"),
# #                 html.H2(id=id_),
# #             ]
# #         ),
# #         # ensure the card expands vertically nicely
# #         className="state-latest-price",
# #     )
# # # a row at the top of the right column to show the KPI card
# # kpi_row = dbc.Row(
# #     [
# #         dbc.Col(price_card("kpi-median-price")),
# #     ])

# # #shows the exact value for the selected year/month for the chosen state
# # bottom_readout = dbc.Card(
# #     dbc.CardBody([
# #         html.H6("Selected Month Value"),
# #         html.Div(id="selected-month-value"),
# #     ])
# # )

# # # --- Percent change & IRR 
# # # card shows percent change from selected month to the latest
# # percent_change_card = dbc.Card(
# #     dbc.CardBody([
# #         html.H6("Percent Change (Selected → Current)"),
# #         html.Div(id="pct-change"),
# #         html.Hr(),
# #         html.H6("IRR (Selected → Current)"),
# #         html.Div(id="irr-text"),
# #     ])
# # )

# # #line chart to visualize price change
# # trend_line_card = dbc.Card(
# #     dbc.CardBody([
# #         html.H6("Price Trend (Selected → Current)"),
# #         dcc.Graph(id="pct-line"),
# #     ])
# # )

# # # --- Layout------
# # layout = dbc.Container(
# #     [
# #         navbar,
# #         dbc.Row(
# #             [
# #                 dbc.Col(controls, width=2),
# #                 dbc.Col(trend_line_card, width = 7),
# #                 dbc.Col(
# #                     [
# #                         kpi_row,
# #                         dbc.Row(
# #                             [
# #                                 dbc.Col(bottom_readout),
# #                                 dbc.Col(percent_change_card),
# #                             ],),
# #                     ],
# #                 ),
# #             ],
# #         ),
# #     ],
# #     fluid=True,
# # )

# # # ---------- Callbacks ----------

# # # --- only show months that exist in your data for that year
# # @callback(
# #     Output("month-dropdown", "options"), 
# #     Output("month-dropdown", "value"),   
# #     Input("year-dropdown", "value"),    
# # )

# # def sync_month_options(selected_year):
# #     months = year_to_months.get(selected_year, [])
# #     options = [{"label": calendar.month_name[m], "value": m} for m in months]
# #     value = months[-1] if months else None
# #     return options, value

# # # --- Update the KPI (latest value),  the % change, the IRR, and the line figure.
# # @callback(
# #     Output("kpi-median-price", "children"), 
# #     Output("selected-month-value", "children"),  
# #     Output("pct-change", "children"),  
# #     Output("irr-text", "children"),  
# #     Output("pct-line", "figure"), 
# #     Input("state-dropdown", "value"), 
# #     Input("year-dropdown", "value"), 
# #     Input("month-dropdown", "value"),  
# #     Input("refresh", "n_clicks"), 
# # )

# # def update_kpi(selected_state, sel_year, sel_month, _):
# #     # --- Step 1: get selected state column ---
# #     if selected_state not in df.columns:
# #         kpi_text = month_text = pct_text = irr_text = "State not found"
# #         return kpi_text, month_text, pct_text, irr_text, px.line()

# #     selected_col = df[selected_state]  
# #     latest_val = selected_col.iloc[-1]
# #     kpi_text = f"${latest_val:,.0f}" if pd.notna(latest_val) else "—"

# #     # --- Step 2: check for year/month selection ---
# #     if not sel_year or not sel_month:
# #         return kpi_text, "Select a year and month", "Select a year and month", "Select a year and month", px.line()

# #     # --- Step 3: get the timestamp for selected year/month ---
# #     col_name = ym_to_col.get((int(sel_year), int(sel_month)))

# #     # --- Step 4: handle missing data ---
# #     if col_name is None or pd.isna(selected_col.get(col_name, None)):
# #         month_text = f"{selected_state} — {calendar.month_name[int(sel_month)]} {sel_year}: —"
# #         pct_text = f"{selected_state}: —"
# #         irr_text = f"{selected_state}: —"
# #         return kpi_text, month_text, pct_text, irr_text, px.line()

# #     # --- Step 5: get value for selected month ---
# #     sel_val = selected_col[(selected_col.index.year == int(sel_year)) & (selected_col.index.month == int(sel_month))].iloc[0]
# #     month_text = f"{selected_state} — {calendar.month_name[int(sel_month)]} {sel_year}: ${sel_val:,.0f}"

# #     # --- Step 6: percent change ---
# #     if sel_val == 0 or pd.isna(latest_val):
# #         pct_text = f"{selected_state}: N/A (insufficient data)"
# #     else:
# #         pct = (latest_val - sel_val) / sel_val * 100.0
# #         pct_text = f"{selected_state}: {pct:+.2f}% since {calendar.month_name[int(sel_month)][:3]} {sel_year}"

# #     # --- Step 7: annualized IRR ---
# #     months_diff = (latest_dt.year - int(sel_year)) * 12 + (latest_dt.month - int(sel_month))
# #     if months_diff <= 0 or sel_val <= 0 or pd.isna(latest_val):
# #         irr_text = f"{selected_state}: IRR N/A (insufficient or invalid data)"
# #     else:
# #         annualized_irr = (latest_val / sel_val) ** (12.0 / months_diff) - 1.0
# #         irr_text = f"{selected_state}: {annualized_irr*100:.2f}% annualized"

# #     # --- Step 8: time series for plotting ---
# #     start_dt = pd.Timestamp(year=int(sel_year), month=int(sel_month), day=1)
# #     ts_window = selected_col[(selected_col.index >= start_dt) & (selected_col.index <= latest_dt)]

# #     # --- Step 9: create Plotly figure ---
# #     fig = px.line(
# #         x=ts_window.index,
# #         y=ts_window.values,
# #         labels={"x": "Date", "y": "Median House Price ($)"},
# #         title=None
# #     )
# #     fig.update_layout(margin=dict(t=10, r=10, b=10, l=10), height=280, hovermode="x unified")
# #     fig.update_yaxes(tickprefix="$", separatethousands=True)

# #     print(f"Selected state: {selected_state}, Year/Month: {sel_year}/{sel_month}")
# #     print(f"Latest val: {latest_val}, Selected val: {sel_val}")
# #     print(f"ts_window length: {len(ts_window)}")
    
# #     # --- Step 10: return all results ---
# #     return kpi_text, month_text, pct_text, irr_text, fig

# # # # --- Run it
# # # if __name__ == "__main__":
# # #     app.run(debug=True)


# import dash
# from dash import html
# from dash import Dash, dash_table, html, Input, Output, callback, page_container
# import dash_bootstrap_components as dbc
# import pandas as pd

# dash.register_page(__name__, path="/", name="Home")
# #app= Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# import base64

# df= pd.DataFrame([
#     {"Name":"Violet Zhao", "Email":"yzhao32@wm.edu", "Home":"Beijing"},
#     {"Name":"Rachel Cole", "Email":"rmcole@wm.edu", "Home":"California"},
#     {"Name":"Josh Vasquez", "Email":"jsvasqeuz01@wm.edu", "Home":"Virginia"},
#     {"Name":"Cade Haskins", "Email":"cadehaskins@wm.edu", "Home":"Minnesota"}])



# # imgVfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgV.jpeg"
# imgVfile= "data/imgV.jpeg"

# with open(imgVfile, "rb") as image_file:
#     imgV_data = base64.b64encode(image_file.read())
#     imgV_data = imgV_data.decode()
#     imgV_data = "{}{}".format("data:image/jpg;base64, ", imgV_data)


# # imgVPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgVP.jpg"
# imgVPfile= "data/imgVP.jpg"

# with open(imgVPfile, "rb") as image_file:
#     imgVP_data = base64.b64encode(image_file.read())
#     imgVP_data = imgVP_data.decode()
#     imgVP_data = "{}{}".format("data:image/jpg;base64, ", imgVP_data)

# # imgRPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgRP.jpg"
# imgRPfile= "data/imgRP.jpg"

# with open(imgRPfile, "rb") as image_file:
#     imgRP_data = base64.b64encode(image_file.read())
#     imgRP_data = imgRP_data.decode()
#     imgRP_data = "{}{}".format("data:image/jpg;base64, ", imgRP_data)

# # imgJPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgJP.jpg"
# imgJPfile= "data/imgJP.jpg"

# with open(imgJPfile, "rb") as image_file:
#     imgJP_data = base64.b64encode(image_file.read())
#     imgJP_data = imgJP_data.decode()
#     imgJP_data = "{}{}".format("data:image/jpg;base64, ", imgJP_data)

# # imgCPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\CP.jpg"
# imgCPfile= "data/imgCP.jpg"

# with open(imgCPfile, "rb") as image_file:
#     imgCP_data = base64.b64encode(image_file.read())
#     imgCP_data = imgCP_data.decode()
#     imgCP_data = "{}{}".format("data:image/jpg;base64, ", imgCP_data)


# layout= dbc.Container([
# dbc.Row(html.Div("VRJC Reality",
#                         style={"margin":"0","backgroundColor": "#293831", "padding": "40px","color":"#CDD6D3",
#                                 "textAlign": "center", "font-size":"35px"}),),
               
# dbc.Row(html.P("As a part of the MSBA class you will soon be applying for positions at high end firms throught the country, or possibly the globe. To help you get an idea of the current housing market, we have provided median home prices for all 50 states in the U.S.A. As well as an interactive page with median prices for every city in China."),
#         ),

# dbc.Row(html.H3("Meet our team!", style={"textAlign":"center"})),

# dbc.Row([

#             dbc.Col(html.Img(
#              id="tag_id",
#              src=imgVP_data,
#              alt="my image",
        
#              height="300",
#              className="img_class"), width=3),

#             dbc.Col(html.Img(
#              id="tag1_id",
#              src=imgRP_data,
#              alt="my image",
             
#              height="300",
#              className="img_class"), width=3),

#             dbc.Col(html.Img(
#              id="tag2_id",
#              src=imgJP_data,
#              alt="my image",
             
#              height="300",
#              className="img_class"), width=3),

#             dbc.Col(html.Img(
#              id="tag3_id",
#              src=imgCP_data,
#              alt="my image",
            
#              height="300",
#              className="img_class"), width=3),
#         ]),

# html.Br(),
# html.H6("Team Members"),
# dash.dcc.Dropdown(
#     id="team-drop",
#     options=[{"label": name, "value": name} for name in df['Name']],
#     placeholder="Choose a team member...",
#     value=None,
#     clearable=True,
#     style={"marginBottom": "1em"}),
#  html.Div(id="team-info")
         

#     ], fluid=True)

# @callback(
#     Output("team-info", "children"),
#     Input("team-drop", "value")
# )

# def display_team_info(selected_name):
#     if not selected_name:
#         return "Select a member to view details."
#     member = df[df["Name"] == selected_name].iloc[0]
#     return dbc.Card([
#         dbc.CardHeader(member["Name"]),
#         dbc.CardBody([
#             html.P(f"Email: {member['Email']}"),
#             html.P(f"Home: {member['Home']}")
#         ])
#     ], style={"width": "22rem", "marginTop": "1em"})





# #if __name__ == "__main__":
# #    app.run(debug=True)


import requests
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, register_page
import dash
import plotly.express as px
from pathlib import Path
import dash_bootstrap_components as dbc
#both bewlow help with calendra 
import calendar
from collections import defaultdict
import numpy as np
##from statsmodels.tsa.arima.model import ARIMA # type: ignore

# --- Load the Zillow state CSV from disk.
# read the CSV containing state-level median home prices with monthly columns

dash.register_page(__name__, path='/states',name='page1')

#DATA_PATH = Path(__file__).resolve().parent.parent /"data" / "US_median_house_state.csv"
#df = pd.read_csv(DATA_PATH)


# turn all monthly columns to numeric values
df = pd.read_csv("data/US_Median_Housing_Prices.csv", header=0, index_col=0)


# df[date_cols] = df[date_cols].apply(pd.to_numeric, errors="coerce")
# df.index = pd.to_numeric(df.index, errors="coerce")

#----- Making the Month and years available -----
# month/year selection limited to your data range.
df.index = pd.to_datetime(df.index, format="%m/%d/%Y", errors="coerce")
date_index = df.index
# date_index = pd.to_datetime(df.index, format="%m/%d/%Y", errors="coerce")

#loop to look through csv
ym_to_col = {}
for d in date_index.dropna():
    key = (d.year, d.month)
    ym_to_col[key] = d

# create a sorted list choicef or dropdown
years = sorted({d.year for d in date_index if pd.notna(d)})
# sorted months 
year_to_months = defaultdict(set)
# accumulate all months per year with a number for that year(1,2,3...)
for d in date_index.dropna():
    year_to_months[d.year].add(d.month)
# year's month set into a sorted list for clean dropdown options
for y in list(year_to_months.keys()):
    year_to_months[y] = sorted(year_to_months[y])



# compute the most recent available month in the dataset for defaults
latest_dt = max(d for d in date_index if pd.notna(d))
# store default year from the latest timestamp
years_all = years 
default_year = years_all[-3] if len(years_all) >= 3 else years_all[-1]

# store default month from the latest timestamp
default_month = latest_dt.month

# --- States for dropdown.---------
# build a sorted list of state names from the RegionName column
states = sorted(df.columns)

# ---------- App ----------
# create the Dash app and include Bootstrap CSS for styling
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- Top bar.
# define a simple top navigation bar with a title and subtitle
navbar = html.Div(
    [
        # main heading text
        html.H2("US States Median House Price", className="state-main-header"),
        # subheading text
        html.Span("Public API", className="state-sub-header"),
    ],
    # little style before we change it in the style css
    className="navbar navbar-light bg-white mb-4 px-3 justify-content-between align-items-center",
)

# --- Controls (state dropdown + month/year dropdowns)-------
# build a controls card containing the state and month/year selection widgets
controls = dbc.Card(
    [
        # card header text
        dbc.CardHeader("Controls"),
        # card body containing interactive inputs
        dbc.CardBody(
            [
                # label above the state dropdown
                dbc.Label("State"),
                # dropdown of all states (RegionName) with a default of CA if present
                dcc.Dropdown(
                    id="state-dropdown",
                    options=[{"label": s, "value": s} for s in states],
                    value="Virginia" if "Virginia" in states else states[0],
                    clearable=False,
                ),
                # label above the year dropdown
                dbc.Label("Year"),
                # dropdown for year
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[{"label": str(y), "value": y} for y in years],
                    value=default_year,
                    clearable=False,
                ),
                # label above the month dropdown
                dbc.Label("Month"),
                # dropdown for month
                dcc.Dropdown(
                    id="month-dropdown",
                    options=[{"label": calendar.month_name[m], "value": m} for m in year_to_months[default_year]],
                    value=default_month,
                    clearable=False,
                ),
                # a little spacing before the refresh button
                html.Br(),
                # refresh button 
                dbc.Button("Refresh", id="refresh", n_clicks=0,),
                # horizontal break to separate controls 
                html.Hr(),
                # small text showing the data source
                html.Small("Data source: Zillow.com."),
            ]
        ),
    ],
    # spacing class to separate the controls card from other elements
    className="state-dropdown-controls",
)

# --- KPI card that shows the latest value--------
def price_card(id_):
    # create a Bootstrap card
    return dbc.Card(
        # card body contains the texts
        dbc.CardBody(
            [
                html.H6("Latest Mean House Price"),
                html.H2(id=id_),
            ]
        ),
        # ensure the card expands vertically nicely
        className="state-latest-price",
    )
# a row at the top of the right column to show the KPI card
kpi_row = dbc.Row(
    [
        dbc.Col(price_card("kpi-median-price")),
    ])

#shows the exact value for the selected year/month for the chosen state
bottom_readout = dbc.Card(
    dbc.CardBody([
        html.H6("Selected Month Value"),
        html.Div(id="selected-month-value"),
    ])
)

# --- Percent change & IRR 
# card shows percent change from selected month to the latest
percent_change_card = dbc.Card(
    dbc.CardBody([
        html.H6("Percent Change (Selected → Current)"),
        html.Div(id="pct-change"),
        html.Hr(),
        html.H6("IRR (Selected → Current)"),
        html.Div(id="irr-text"),
    ])
)

#line chart to visualize price change
trend_line_card = dbc.Card(
    dbc.CardBody([
        html.H6("Price Trend (Selected → Current)"),
        dcc.Graph(id="pct-line"),
    ])
)

# --- Layout------
layout = dbc.Container(
    [
        html.H3("United Sate Price Dashboard", className="mt-3 mb-3"),
        dbc.Row(
            [
                dbc.Col(controls, width=3),
                dbc.Col(
                    [
                        kpi_row,
                        html.Br(),
                        bottom_readout,
                        html.Br(),
                        percent_change_card,
                        html.Br(),
                        trend_line_card,
                        # dbc.Row(
                        #     [
                        #         dbc.Col(growth_card, md=6),
                        #         dbc.Col(chart_card, md=6),
                        #     ],
                        #     className="gy-3"
                        # ),
                    ],
                    width=9
                ),
            ],
            className="g-3",
            align='stretch'
        )
    ],
    fluid=True
)


# ---------- Callbacks ----------

# --- only show months that exist in your data for that year
@callback(
    Output("month-dropdown", "options"), 
    Output("month-dropdown", "value"),   
    Input("year-dropdown", "value"),    
)

def sync_month_options(selected_year):
    months = year_to_months.get(selected_year, [])
    options = [{"label": calendar.month_name[m], "value": m} for m in months]
    value = months[-1] if months else None
    return options, value

# --- Update the KPI (latest value),  the % change, the IRR, and the line figure.
@callback(
    Output("kpi-median-price", "children"), 
    Output("selected-month-value", "children"),  
    Output("pct-change", "children"),  
    Output("irr-text", "children"),  
    Output("pct-line", "figure"), 
    Input("state-dropdown", "value"), 
    Input("year-dropdown", "value"), 
    Input("month-dropdown", "value"),  
    Input("refresh", "n_clicks"), 
)

def update_kpi(selected_state, sel_year, sel_month, _):
    # --- Step 1: get selected state column ---
    if selected_state not in df.columns:
        kpi_text = month_text = pct_text = irr_text = "State not found"
        return kpi_text, month_text, pct_text, irr_text, px.line()

    selected_col = df[selected_state]  
    latest_val = selected_col.iloc[-1]
    kpi_text = f"${latest_val:,.0f}" if pd.notna(latest_val) else "—"

    # --- Step 2: check for year/month selection ---
    if not sel_year or not sel_month:
        return kpi_text, "Select a year and month", "Select a year and month", "Select a year and month", px.line()

    # --- Step 3: get the timestamp for selected year/month ---
    col_name = ym_to_col.get((int(sel_year), int(sel_month)))

    # --- Step 4: handle missing data ---
    if col_name is None or pd.isna(selected_col.get(col_name, None)):
        month_text = f"{selected_state} — {calendar.month_name[int(sel_month)]} {sel_year}: —"
        pct_text = f"{selected_state}: —"
        irr_text = f"{selected_state}: —"
        return kpi_text, month_text, pct_text, irr_text, px.line()

    # --- Step 5: get value for selected month ---
    sel_val = selected_col[(selected_col.index.year == int(sel_year)) & (selected_col.index.month == int(sel_month))].iloc[0]
    month_text = f"{selected_state} — {calendar.month_name[int(sel_month)]} {sel_year}: ${sel_val:,.0f}"

    # --- Step 6: percent change ---
    if sel_val == 0 or pd.isna(latest_val):
        pct_text = f"{selected_state}: N/A (insufficient data)"
    else:
        pct = (latest_val - sel_val) / sel_val * 100.0
        pct_text = f"{selected_state}: {pct:+.2f}% since {calendar.month_name[int(sel_month)][:3]} {sel_year}"

    # --- Step 7: annualized IRR ---
    months_diff = (latest_dt.year - int(sel_year)) * 12 + (latest_dt.month - int(sel_month))
    if months_diff <= 0 or sel_val <= 0 or pd.isna(latest_val):
        irr_text = f"{selected_state}: IRR N/A (insufficient or invalid data)"
    else:
        annualized_irr = (latest_val / sel_val) ** (12.0 / months_diff) - 1.0
        irr_text = f"{selected_state}: {annualized_irr*100:.2f}% annualized"

    # --- Step 8: time series for plotting ---
    start_dt = pd.Timestamp(year=int(sel_year), month=int(sel_month), day=1)
    ts_window = selected_col[(selected_col.index >= start_dt) & (selected_col.index <= latest_dt)]

    # --- Step 9: create Plotly figure ---
    fig = px.line(
        x=ts_window.index,
        y=ts_window.values,
        labels={"x": "Date", "y": "Median House Price ($)"},
        title=None
    )
    fig.update_layout(margin=dict(t=10, r=10, b=10, l=10), height=280, hovermode="x unified")
    fig.update_yaxes(tickprefix="$", separatethousands=True)

    print(f"Selected state: {selected_state}, Year/Month: {sel_year}/{sel_month}")
    print(f"Latest val: {latest_val}, Selected val: {sel_val}")
    print(f"ts_window length: {len(ts_window)}")
    
    # --- Step 10: return all results ---
    return kpi_text, month_text, pct_text, irr_text, fig

# # --- Run it
# if __name__ == "__main__":
#     app.run(debug=True)