import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc




slider_list = [dict(step=10, min=0, max=2000, value=1000, var='N', name='N: number of plants (in absence of virus)'),
                dict(step=0.01, min=0, max=0.1, value=0.01, var='rho', name=u'\u03C1: natural plant death rate'),
                dict(step=0.01, min=0, max=0.2, value=0.01, var='mu', name=u'\u03BC: roguing rate/disease induced mortality'),
                dict(step=0.01, min=0, max=1, value=0.12, var='alpha', name=u'\u03B1: vector death due to flights'),
                dict(step=0.1, min=0, max=10, value=4, var='tau', name=u'\u03C4: vectors losing infectivity'),
                dict(step=0.01, min=0, max=1, value=0.18, var='sigma', name=u'\u03C3: per capita vector birth rate (at low density)'),
                dict(step=0.1, min=0, max=2200, value=1977.6, var='zeta', name=u'\u03B6: vector population density dependent threshold'),
                dict(step=0.1, min=0, max=4, value=2, var='Gamma', name=u'\u0393: average time feeding per settled landing'),
                dict(step=0.1, min=0, max=1, value=0, var='delta', name=u'\u03B4: increase in death rate as more plants visited per feed'),
                dict(step=0.1, min=0, max=3, value=1, var='beta', name=u'\u03B2: change in birth rate on infected plants'),
                dict(step=0.1, min=0, max=4, value=1, var='nu_m', name=u'\u03BD\u208B: bias of non-viruliferous vectors to land on infected plants'),
                dict(step=0.1, min=0, max=4, value=1, var='nu_p', name=u'\u03BD\u208A: bias of viruliferous vectors to land on infected plants'),
                dict(step=0.1, min=0, max=1, value=0.5, var='om_m', name=u'\u03C9\u208B: probability non-viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.1, min=0, max=1, value=0.5, var='om_p', name=u'\u03C9\u208A: probability viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.1, min=0, max=2, value=1, var='eps_m', name=u'\u03B5\u208B: bias of non-viruliferous vector to feed on infected plant'),
                dict(step=0.1, min=0, max=2, value=1, var='eps_p', name=u'\u03B5\u208A: bias of viruliferous vector to feed on infected plant'),
                # dict(step=0.1, min=0, max=1, value=1, var='gamma', name=u'\u03B3: probability that uninfected plant is inoculated by viruliferous vector on single visit'),
                # dict(step=0.1, min=0, max=1, value=1, var='eta', name=u'\u03B7: probability non-viruliferous vector acquires virus in single visit to infected plant'),
                dict(step=0.02, min=0, max=1, value=0.02, var='host-inc-0', name=u'I\u2080/(S\u2080+I\u2080): initial host incidence'),
                dict(step=0.02, min=0, max=1, value=1, var='N-frac', name=u'Initial host amount (as a fraction of N)'),
                dict(step=0.02, min=0, max=1, value=0.02, var='vec-inc-0', name=u'Z\u2080/(X\u2080+Z\u2080): initial vector incidence'),
                dict(step=0.02, min=0, max=1, value=1, var='kapp-frac', name=u'Initial vector amount (as a fraction of \u03BA)'),
                ]




def get_sliders(sldr_list, prefix):
    return [html.Div([
                    html.P(x['name'], className="control-label"),
                    
                    dcc.Slider(
                        min=x['min'],
                        max=x['max'],
                        step=x['step'],
                        value=x['value'],
                        marks={i: f'{i}' for i in [x['min'], x['max']]},
                        id=f"{prefix}slider-{x['var']}",
                        tooltip = {
                            'always_visible': False,
                            'placement': "bottom",
                            }
                    )
                ],
                className="control-wrapper"
                    ) for x in sldr_list]




def get_ctrl_group(title, index, prefix, *controls):
    return html.Div([
                html.Div([
                    html.H4(title, className="control-collapse-title"),
                    html.Div(
                        html.Img(src='/assets/images/down_icon.svg',
                        className="down-arrow"
                        )),
                    ],
                    id=f"{prefix}sld-bt-{index}", 
                    className="text-with-arrow"),
                
                dbc.Collapse(
                    controls,
                    id=f"{prefix}sld-gp-{index}",
                    is_open=False)
                ])

def get_par_choice(prefix):
    return html.Div([
                html.P("Parameter choice", className="control-label"),
                
                dcc.RadioItems(
                    id=f"{prefix}param-choice",
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
            )