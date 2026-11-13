# Inbuilt
import json

# Third Party
import dash
import dash_split
import dash_bootstrap_components as dbc
import pandas
import plotly.express as px

with open("test.txt") as file:
    test_data = json.loads(file.read())

architecture = {
    "header": [
        dash.html.H1(
            children="{}'s Personal Dashboard".format(test_data["global"]["name"]), 
            style={"textAlign":"center"}
        ),
        dash.dcc.Dropdown(
            options=sorted(test_data["legends"]["all"].keys()), 
            value=sorted(test_data["legends"]["all"].keys())[0],
            id="legend_selection",
            searchable=False,
        ),
        dash.dcc.Tabs(
            id="tabs",
            value="legend_overview",
            children=[
                dash.dcc.Tab(label="Legend Overview",value="legend_overview"),
                dash.dcc.Tab(label="Player Overview",value="player_overview"),
            ]
        ),
    ],

    "tabs": {

        "legend_overview": [
            dash.html.Div(
                [                
                    dash.html.Img(
                        id="legend_icon",
                    ),
                    dash.html.Div(
                        id="legend_stats",
                        children=[]
                    )
                ],
                style={
                    "display": "flex", 
                    "flexDirection": "row", 
                    "margin": "0 auto",
                },
            )
        ],

        "player_overview": [
            dash_split.Split(
                direction="horizontal",
                gutterAlign="center",
                children=[
                    dbc.Col(
                        [
                            dash.html.Div("Username: [{}] {}".format(test_data["global"]["tag"], test_data["global"]["name"])),
                            dash.html.Div("Platform: {}".format(test_data["global"]["platform"])),
                            dash.html.Div("ID: {}".format(test_data["global"]["uid"])),
                        ],
                    ),
                    dbc.Col(
                        [
                            dash.html.Div("Player level ({}/500):".format(test_data["global"]["level"])),
                            dash.dcc.Graph(
                                figure=px.pie(
                                    values=[
                                        test_data["global"]["level"],
                                        500 - test_data["global"]["level"],
                                    ],
                                    names=[
                                        "LEVEL",
                                        "LEFT",
                                    ]
                                )
                            )
                        ],
                    ),
                ]
            ),
        ],
    },
}

app = dash.Dash()

app.layout = dbc.Container(
    [
        *architecture["header"],
        dbc.Row(
            id="tab_contents",
            children=[],
        )
    ]
)