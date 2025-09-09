import dash
from dash import Dash, html, dcc, callback, Input, Output, register_page
import pandas as pd
import requests
import plotly.express as px
from pathlib import Path
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

register_page(__name__, path='/CoL', title='Salary to Prices', name='Salary to Prices')

# DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "state_annual_.csv"

#Read the files and prepped them to be read
salary_df = pd.read_csv("data/job_salaries.csv", index_col=0)
housing_df = pd.read_csv("data/2025_Median_Housing_Prices.csv")

job_list = salary_df.index
print(salary_df.index)
DEFAULT_VALUE = job_list[0] 

controls_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Controls", className="mb-3"),

            dbc.Label("Jobs"),   
            dcc.Dropdown(
                id="intl-job",
                options=[{"label": j, "value": j} for j in job_list],
                value=DEFAULT_VALUE,
                clearable=False,
                style={"marginBottom": "12px"}
            ),

           
            dbc.Button("Refresh", 
                       id="refresh", 
                       n_clicks=0, 
                       color="primary", 
                       className="mt-2 mx-auto d-block",
                       style={"padding": "1.2vw 1.7vw", "margin-bottom": "300px"}),

            html.Hr(),
            html.Small("Data source: Zip Recruiter", 
                       className="text-muted",
                       style={"marginTop": "auto"}),
        ], 
    ),
    className="bg-light"
)

chart_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Average Salary to Housing Prices (2025)"),
            dcc.Loading(
                dcc.Graph(id="intl-bar", style={"height": "60vh"}, config={"displayModeBar": False}),
                
                type="default"
            )
        ]
    )
)

layout = dbc.Container(
    [
        html.H3("Price Dashboard", className="mt-3 mb-3"),
        dbc.Row(
            [
                dbc.Col(controls_card, width=3),
                dbc.Col([chart_card], width=9),
            ],
            className="g-3",
            align='stretch'
        )
    ],
    fluid=True
)

## Functions 

def calc_salary_housing_ratio(salary, housing, job):

    #Check for missing values
    ratio_dict = {}

    for state in salary.columns:
        hous = housing[state].iloc[0]
        sal = salary.loc[job, state]
        if pd.isnull(sal) or pd.isnull(hous):
            ratio_dict[state] = -1
        else:
            ratio_dict[state] = float(hous) / float(sal)
    
    temp_df = pd.DataFrame.from_dict(ratio_dict, orient='index', columns=['Housing/Salary Ratio'])
    temp_df_sorted = temp_df.sort_values(by="Housing/Salary Ratio")
    return temp_df_sorted

temp = ratio_df = calc_salary_housing_ratio(salary_df, housing_df, 'Consultant')
print(temp.index)
## Callbacks

@callback(
   
    Output("intl-bar", "figure"),
    Input("intl-job", "value"),
    Input("refresh", "n_clicks")
)


# def update_graph(job, _n_clicks):

#     if not job or salary_df.empty or housing_df.empty:

#         fig = px.bar(title="No data")
#         return fig

#     ratio_df = calc_salary_housing_ratio(salary_df, housing_df, job)

#     fig = px.bar(
#         ratio_df,
#         x = ratio_df.index,
#         y = "Housing/Salary Ratio",

#     )

def update_graph(job, _n_clicks):
    if not job or salary_df.empty or housing_df.empty:
        fig = px.bar(title="No data")
        return fig

    ratio_df = calc_salary_housing_ratio(salary_df, housing_df, job)

    fig = px.bar(
        ratio_df,
        x=ratio_df.index,  # state names
        y="Housing/Salary Ratio",  # the column values
        labels={"x": "State", "Housing/Salary Ratio": "Ratio"},
        title=f"Housing-to-Salary Ratio for {job}",
    )

    fig.update_layout(
        xaxis_title="State",
        yaxis_title="Housing / Salary Ratio",
        xaxis_tickangle=60,
        # margin=dict(l=40, r=40, t=40, b=120),
        height=800
    )

    fig.update_traces(
        text=ratio_df["Housing/Salary Ratio"].round(2),
        textposition='outside'
    )

    fig.add_shape(
    type="line",
    x0=-0.5, 
    x1=len(ratio_df) - 0.5,  
    y0=3,
    y1=3,
    line=dict(
        color="purple",
        width=2,
        dash="dash"
    )
    )

    fig.add_trace(go.Scatter(
    x=[None], y=[None],  # invisible point
    mode='lines',
    line=dict(color="purple", width=2, dash="dash"),
    name="Recommended Threshold"
    ))
    
    return fig

# if __name__ == "__main__":
#     app.run(debug=True)