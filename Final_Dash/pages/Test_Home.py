import dash
from dash import html
from dash import Dash, dash_table, html, Input, Output, callback, page_container
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/", name="Home")
#app= Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

import base64

df= pd.DataFrame([
    {"Name":"Violet Zhao", "Email":"yzhao32@wm.edu", "Home":"Beijing"},
    {"Name":"Rachel Cole", "Email":"rmcole@wm.edu", "Home":"California"},
    {"Name":"Josh Vasquez", "Email":"jsvasqeuz01@wm.edu", "Home":"Virginia"},
    {"Name":"Cade Haskins", "Email":"cadehaskins@wm.edu", "Home":"Minnesota"}])



# imgVfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgV.jpeg"
imgVfile= "data/imgV.jpeg"

with open(imgVfile, "rb") as image_file:
    imgV_data = base64.b64encode(image_file.read())
    imgV_data = imgV_data.decode()
    imgV_data = "{}{}".format("data:image/jpg;base64, ", imgV_data)


# imgVPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgVP.jpg"
imgVPfile= "data/imgVP.jpg"

with open(imgVPfile, "rb") as image_file:
    imgVP_data = base64.b64encode(image_file.read())
    imgVP_data = imgVP_data.decode()
    imgVP_data = "{}{}".format("data:image/jpg;base64, ", imgVP_data)

# imgRPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgRP.jpg"
imgRPfile= "data/imgRP.jpg"

with open(imgRPfile, "rb") as image_file:
    imgRP_data = base64.b64encode(image_file.read())
    imgRP_data = imgRP_data.decode()
    imgRP_data = "{}{}".format("data:image/jpg;base64, ", imgRP_data)

# imgJPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\imgJP.jpg"
imgJPfile= "data/imgJP.jpg"

with open(imgJPfile, "rb") as image_file:
    imgJP_data = base64.b64encode(image_file.read())
    imgJP_data = imgJP_data.decode()
    imgJP_data = "{}{}".format("data:image/jpg;base64, ", imgJP_data)

# imgCPfile= "C:\\Users\\Owner\\Desktop\\CTBA\\CTBA_Group_2\\Final_Dash\\data\\CP.jpg"
imgCPfile= "data/imgCP.jpg"

with open(imgCPfile, "rb") as image_file:
    imgCP_data = base64.b64encode(image_file.read())
    imgCP_data = imgCP_data.decode()
    imgCP_data = "{}{}".format("data:image/jpg;base64, ", imgCP_data)


layout= dbc.Container([
dbc.Row(html.Div("VRJC Reality",
                        style={"margin":"0","backgroundColor": "#293831", "padding": "40px","color":"#CDD6D3",
                                "textAlign": "center", "font-size":"35px"}),),
               
dbc.Row(html.P("As a part of the MSBA class you will soon be applying for positions at high end firms throught the country, or possibly the globe. To help you get an idea of the current housing market, we have provided median home prices for all 50 states in the U.S.A. As well as an interactive page with median prices for every city in China."),
        ),

dbc.Row(html.H3("Meet our team!", style={"textAlign":"center"})),

dbc.Row([

            dbc.Col(html.Img(
             id="tag_id",
             src=imgVP_data,
             alt="my image",
        
             height="300",
             className="img_class"), width=3),

            dbc.Col(html.Img(
             id="tag1_id",
             src=imgRP_data,
             alt="my image",
             
             height="300",
             className="img_class"), width=3),

            dbc.Col(html.Img(
             id="tag2_id",
             src=imgJP_data,
             alt="my image",
             
             height="300",
             className="img_class"), width=3),

            dbc.Col(html.Img(
             id="tag3_id",
             src=imgCP_data,
             alt="my image",
            
             height="300",
             className="img_class"), width=3),
        ]),

html.Br(),
html.H6("Team Members"),
dash.dcc.Dropdown(
    id="team-drop",
    options=[{"label": name, "value": name} for name in df['Name']],
    placeholder="Choose a team member...",
    value=None,
    clearable=True,
    style={"marginBottom": "1em"}),
 html.Div(id="team-info")
         

    ], fluid=True)

@callback(
    Output("team-info", "children"),
    Input("team-drop", "value")
)

def display_team_info(selected_name):
    if not selected_name:
        return "Select a member to view details."
    member = df[df["Name"] == selected_name].iloc[0]
    return dbc.Card([
        dbc.CardHeader(member["Name"]),
        dbc.CardBody([
            html.P(f"Email: {member['Email']}"),
            html.P(f"Home: {member['Home']}")
        ])
    ], style={"width": "22rem", "marginTop": "1em"})





#if __name__ == "__main__":
#    app.run(debug=True)