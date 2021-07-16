import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import datetime

from dash_html_components.H4 import H4
from utils.figures import MODEBAR_CONFIG


model_controls = html.Div([

        html.H4("Controls", className="uppercase-title"),

        html.Div([
                html.P("Checklist", className="control-label"),
                
                dbc.Checklist(
                    id='checklist',
                    options=[{'label': "Title contains date?", 'value': 'contains-date'},
                            {'label': "Plot in red?", 'value': 'in-red'}],
                    value=[],
                    className="checklist-top",
                ),
        ],
        className="control-wrapper"
        ),
        
        html.Div([
                html.P("Number of points", className="control-label"),
                
                dcc.Slider(
                    min=0,
                    max=20,
                    step=2,
                    value=10,
                    marks={i: f'{i}' for i in range(0,21,4)},
                    id="slider",
                )
        ],
        className="control-wrapper"
        ),

    ], className="controls")







model_page =  html.Div(
    [
    html.H1(
    "Model outputs",
    className="page-title"
    ),

    html.Div([
        
        model_controls,

        html.Div([
        html.H4("", id="model-fig-title", className="uppercase-title"),
        html.Div(dcc.Graph(id='model-fig',
            config = MODEBAR_CONFIG
            ))
        ],
        className="figure-cont"),
        
    ],
    className="model-page"),
    
    ],
    className="page-contents")