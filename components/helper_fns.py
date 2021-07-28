import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc



def get_sliders(sldr_list, prefix):
    return [html.Div([
                    html.P(x['name'], className="control-label"),
                    
                    dcc.Slider(
                        min=x['min'],
                        max=x['max'],
                        step=x['step'],
                        value=x['value'],
                        marks={i: f'{i}' for i in [x['min'], x['max']]},
                        id=f"{prefix}-slider-{x['var']}",
                        tooltip = {
                            'always_visible': False,
                            'placement': "bottom",
                            }
                    )
                ],
                f"{prefix}-slider-comp-wrapper-{x['var']}",
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
                    id=f"{prefix}-sld-bt-{index}", 
                    className="text-with-arrow"),
                
                dbc.Collapse(
                    controls,
                    id=f"{prefix}-sld-gp-{index}",
                    is_open=False)
                ])



def get_par_choice(prefix):
    return html.Div([
                html.P("Parameter choice", className="control-label"),
                
                dcc.RadioItems(
                    id=f"{prefix}-param-choice",
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


def get_modal(prefix):
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("Parameter error"),
                    dbc.ModalBody(id=f"{prefix}-modal-content"),
                ],
                id=f"{prefix}-error-modal",
                className="error-modal",
                is_open=False,
            ),
        ],
        )


def get_run_button(prefix):
    if prefix=="ps":
        button_text = "Run scan"
    else:
        button_text = "Run model"
    
    return html.Div(button_text,
                    className='my-button',
                    id=f"{prefix}-run-button")



def get_dropdown(id_suffix, slider_list, classes):
    return html.Div([
            
            html.P("Variable choice", className="control-label"),
                
            dcc.Dropdown(
                            id=f"ps-variable-choice-{id_suffix}",
                            options=[
                                {'label': var["name"], 'value': var["var"]} 
                                for var in slider_list
                            ],
                            value='mu',
                            clearable = False,
                            searchable=False,
                            optionHeight=60,
                        )
        
            ],
            id=f"ps-var-choice-wrapper-{id_suffix}",
            className=classes
            )


def get_scenario_radio(prefix):
    return html.Div([
            
            html.P("Scenario", className="control-label"),
                
            dcc.RadioItems(
                            id=f"{prefix}-persistent-choice",
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