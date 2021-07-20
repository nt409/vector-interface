import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from utils.figures import MODEBAR_CONFIG


slider_list = [dict(step=10, min=0, max=2000, value=1000, var='N', name='N: Number of plants (in absense of virus)'),
                dict(step=0.01, min=0, max=0.1, value=0.01, var='rho', name=u'\u03C1: Natural plant death rate'),
                dict(step=0.01, min=0, max=0.1, value=0.01, var='mu', name=u'\u03BC: Roguing rate/disease induced mortality'),
                dict(step=0.01, min=0, max=1, value=0.12, var='alpha', name=u'\u03B1: Vector death due to flights'),
                dict(step=0.1, min=0, max=10, value=4, var='tau', name=u'\u03C4: Rate of vectors losing infectivity'),
                dict(step=0.01, min=0, max=1, value=0.18, var='sigma', name=u'\u03C2: Per capita vector birth rate (at low density)'),
                dict(step=0.1, min=0, max=2200, value=1977.6, var='zeta', name=u'\u03B6: Vector population density dependent threshold'),
                dict(step=0.1, min=0, max=4, value=2, var='Gamma', name=u'\u0393: Average time feeding per settled landing'),
                dict(step=0.1, min=0, max=1, value=0, var='delta', name=u'\u03B4: Increase in death rate as more plants visited per feed'),
                dict(step=0.1, min=0, max=1, value=1, var='beta', name=u'\u03B2: Change in birth rate on infected plants'),
                dict(step=0.1, min=0, max=1, value=2, var='nu minus', name=u'\u03BD-: Bias of non-viruliferous vectors to land on infected plants'),
                dict(step=0.1, min=0, max=1, value=2, var='nu plus', name=u'\u03BD+: Bias of viruliferous vectors to land on infected plants'),
                dict(step=0.1, min=0, max=1, value=0.5, var='omega minus', name=u'\u03C9-: Probability non-viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.1, min=0, max=1, value=0.5, var='omega plus', name=u'\u03C9+: Probability viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.1, min=0, max=1, value=2, var='epsilon minus', name=u'\u03B5-: Bias of non-viruliferous vector to feed on infected plant'),
                dict(step=0.1, min=0, max=1, value=2, var='epsilon plus', name=u'\u03B5+: Bias of viruliferous vector to feed on infected plant'),
                dict(step=0.1, min=0, max=1, value=1, var='gamma', name=u'\u03B3: Probability that uninfected plant is inoculated by viruliferous vector on single visit'),
                dict(step=0.1, min=0, max=1, value=1, var='eta', name=u'\u03B7: Probability non-viruliferous vector acquires virus in single visit to infected plant'),
                ]



sliders = [html.Div([
                    html.P(x['name'], className="control-label"),
                    
                    dcc.Slider(
                        min=x['min'],
                        max=x['max'],
                        step=x['step'],
                        value=x['value'],
                        marks={i: f'{i}' for i in [x['min'], x['max']]},
                        id=f"slider-{x['var']}",
                        tooltip = { 'always_visible': True, 'placement': 'bottom'}
                    )
                ],
                className="control-wrapper"
                    ) for x in slider_list]





custom_params = html.Div(
        id="custom-params",
        children=[
    
            html.Span(className="emph-line"),

            html.H4("Custom parameters", className="uppercase-title"),
            
            html.Div([
                html.H4("Host params", className="control-collapse-title"),
                html.Div(
                    html.Img(src='/assets/images/down_icon.svg',
                    className="down-arrow"
                    )),
            ],
            id="sld-bt-1", 
            className="text-with-arrow"),
            
            dbc.Collapse([    
                *sliders[:3],
                ],
                id="sld-gp-1",
                is_open=False),

            html.Div([
                html.H4("Vector params", className="control-collapse-title"),
                html.Div(
                    html.Img(src='/assets/images/down_icon.svg',
                    className="down-arrow"
                    )),
            ],
            id="sld-bt-2", 
            className="text-with-arrow"),

                        
            dbc.Collapse([    
                *sliders[3:10],
                ],
                id="sld-gp-2",
                is_open=False),
            
            
            
            html.Div([
                html.H4("Preference params", className="control-collapse-title"),
                html.Div(
                    html.Img(src='/assets/images/down_icon.svg',
                    className="down-arrow"
                    )),
            ],
            id="sld-bt-3", 
            className="text-with-arrow"),

                        
            dbc.Collapse([    
                *sliders[10:16],
                ],
                id="sld-gp-3",
                is_open=False),
            
            
            html.Div([
                html.H4("Transmission params", className="control-collapse-title"),
                html.Div(
                    html.Img(src='/assets/images/down_icon.svg',
                    className="down-arrow"
                    )),
            ],
            id="sld-bt-4", 
            className="text-with-arrow"),

                        
            dbc.Collapse([    
                *sliders[16:],
                ],
                id="sld-gp-4",
                is_open=False),


        ])


model_controls = html.Div([

        html.Span(className="emph-line"),

        html.H4("Controls", className="uppercase-title"),

        html.Div([
                html.P("Parameter choice", className="control-label"),
                
                dcc.RadioItems(
                    id="param-choice",
                    options=[
                        {'label': ' Default (non-persistent transmission) ', 'value': 'NPT'},
                        {'label': ' Default (persistent transmission) ', 'value': 'PT'},
                        {'label': ' Custom ', 'value': 'C'}
                    ],
                    value='NPT',
                    labelStyle={'display': 'block'}
                ),
        
            ],
            className="control-wrapper"
            ),

        custom_params,

        
    ], className="controls")




figure_cont = html.Div([
            html.Span(className="emph-line"),

            html.H4(" ", id="model-fig-title", className="uppercase-title"),

            html.Div(dcc.Graph(id='model-fig',
                config = MODEBAR_CONFIG
                ))
            ],
            className="figure-cont")





model_page =  html.Div(
    [
    
    html.H1(
        "Model outputs",
        className="page-title"),


    html.Div([
        
        model_controls,

        figure_cont,

        ],
        className="model-page"),
    


    ],
    className="page-contents")