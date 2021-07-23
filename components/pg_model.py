import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from utils.figures import MODEBAR_CONFIG


slider_list = [dict(step=10, min=0, max=2000, value=1000, var='N', name='N: number of plants (in absence of virus)'),
                dict(step=0.01, min=0, max=0.1, value=0.01, var='rho', name=u'\u03C1: natural plant death rate'),
                dict(step=0.01, min=0, max=0.1, value=0.01, var='mu', name=u'\u03BC: roguing rate/disease induced mortality'),
                dict(step=0.01, min=0, max=1, value=0.12, var='alpha', name=u'\u03B1: vector death due to flights'),
                dict(step=0.1, min=0, max=10, value=4, var='tau', name=u'\u03C4: vectors losing infectivity'),
                dict(step=0.01, min=0, max=1, value=0.18, var='sigma', name=u'\u03C3: per capita vector birth rate (at low density)'),
                dict(step=0.1, min=0, max=2200, value=1977.6, var='zeta', name=u'\u03B6: vector population density dependent threshold'),
                dict(step=0.1, min=0, max=4, value=2, var='Gamma', name=u'\u0393: average time feeding per settled landing'),
                dict(step=0.1, min=0, max=1, value=0, var='delta', name=u'\u03B4: increase in death rate as more plants visited per feed'),
                dict(step=0.1, min=0, max=3, value=1, var='beta', name=u'\u03B2: change in birth rate on infected plants'),
                dict(step=0.1, min=0, max=4, value=1, var='nu minus', name=u'\u03BD\u208B: bias of non-viruliferous vectors to land on infected plants'),
                dict(step=0.1, min=0, max=4, value=1, var='nu plus', name=u'\u03BD\u208A: bias of viruliferous vectors to land on infected plants'),
                dict(step=0.1, min=0, max=1, value=0.5, var='omega minus', name=u'\u03C9\u208B: probability non-viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.1, min=0, max=1, value=0.5, var='omega plus', name=u'\u03C9\u208A: probability viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.1, min=0, max=2, value=1, var='epsilon minus', name=u'\u03B5\u208B: bias of non-viruliferous vector to feed on infected plant'),
                dict(step=0.1, min=0, max=2, value=1, var='epsilon plus', name=u'\u03B5\u208A: bias of viruliferous vector to feed on infected plant'),
                # dict(step=0.1, min=0, max=1, value=1, var='gamma', name=u'\u03B3: probability that uninfected plant is inoculated by viruliferous vector on single visit'),
                # dict(step=0.1, min=0, max=1, value=1, var='eta', name=u'\u03B7: probability non-viruliferous vector acquires virus in single visit to infected plant'),
                dict(step=0.02, min=0, max=1, value=0.02, var='host-inc-0', name=u'I\u2080/(S\u2080+I\u2080): initial host incidence'),
                dict(step=0.02, min=0, max=1, value=1, var='N-frac', name=u'Initial host amount (as a fraction of N)'),
                dict(step=0.02, min=0, max=1, value=0.02, var='vec-inc-0', name=u'Z\u2080/(X\u2080+Z\u2080): initial vector incidence'),
                dict(step=0.02, min=0, max=1, value=1, var='kapp-frac', name=u'Initial vector amount (as a fraction of \u03BA)'),
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
                        tooltip = {
                            'always_visible': False,
                            'placement': "bottom",
                            }
                    )
                ],
                className="control-wrapper"
                    ) for x in slider_list]



PT_or_not = html.Div([
            
            html.P("Scenario", className="control-label"),
                
            dcc.RadioItems(
                            id="persistent-choice",
                            options=[
                                {'label': ' Non-persistent transmission ', 'value': 'NPT'},
                                {'label': ' Persistent transmission ', 'value': 'PT'},
                            ],
                            value='NPT',
                            labelStyle={'display': 'block'}
                        )
        
            ],
            className="control-wrapper"
            )


def param_group(title, index, *controls):
    return html.Div([
                html.Div([
                    html.H4(title, className="control-collapse-title"),
                    html.Div(
                        html.Img(src='/assets/images/down_icon.svg',
                        className="down-arrow"
                        )),
                    ],
                    id=f"sld-bt-{index}", 
                    className="text-with-arrow"),
                
                dbc.Collapse(
                    controls,
                    id=f"sld-gp-{index}",
                    is_open=False)
                ])

pg1 = param_group("Host parameters", 1, *sliders[:3])
pg2 = param_group("Vector parameters", 2, *sliders[3:10])
pg3 = param_group("Preference parameters", 3, *sliders[10:16])
# pg4 = param_group("Transmission parameters", 4, *sliders[16:18])
pg5 = param_group("Initial conditions", 5, *sliders[16:])

custom_params = html.Div(
        id="custom-params",
        children=[
    
            html.Span(className="emph-line"),

            html.H4("Custom parameters", className="uppercase-title"),

            PT_or_not,

            pg1,
            pg2,
            pg3,
            # pg4,
            pg5,

        ])


model_controls = html.Div([

        html.Span(className="emph-line"),

        html.H4("Controls", className="uppercase-title"),

        html.Div([
                html.P("Parameter choice", className="control-label"),
                
                dcc.RadioItems(
                    id="param-choice",
                    options=[
                        {'label': ' Default (non-persistent transmission) ', 'value': 'def-NPT'},
                        {'label': ' Default (persistent transmission) ', 'value': 'def-PT'},
                        {'label': ' Custom ', 'value': 'def-C'}
                    ],
                    value='def-NPT',
                    labelStyle={'display': 'block'}
                ),
        
            ],
            className="control-wrapper"
            ),

        custom_params,

        
    ], className="controls")




figure_cont = html.Div([

            #
            html.Span(className="emph-line"),
            html.H4("host dynamics", className="uppercase-title"),

            html.Div(dcc.Graph(id='host-fig',
                config = MODEBAR_CONFIG,
                className="fig-cont"
                )),
            
            #
            html.Span(className="emph-line"),
            html.H4("vector dynamics", className="uppercase-title"),

            html.Div(dcc.Graph(id='vector-fig',
                config = MODEBAR_CONFIG,
                className="fig-cont"
                )),
            
            #
            html.Span(className="emph-line"),
            html.H4("incidence dynamics", className="uppercase-title"),

            html.Div(dcc.Graph(id='incidence-fig',
                config = MODEBAR_CONFIG,
                className="fig-cont"
                )),

            #
            html.Span(className="emph-line"),
            html.H4("Equilibria", className="uppercase-title"),
            html.Div(id="eqm-table-cont", className="table-container"),
            
            #
            html.Span(className="emph-line"),
            html.H4("Model quantities", className="uppercase-title"),
            html.Div(id="R0-k-table-cont", className="table-container"),
            
            #

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