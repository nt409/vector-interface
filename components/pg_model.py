import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from utils.figures import MODEBAR_CONFIG

from components.slr_list import SLIDER_LIST, SLIDER_IND_MAP
from components.helper_fns import get_ctrl_group, get_sliders, \
    get_par_choice, get_modal, get_scenario_radio

m_sliders = get_sliders(SLIDER_LIST, "m")

m_PT_or_not = get_scenario_radio("m")

param_choice = get_par_choice("m")


IM = SLIDER_IND_MAP

pg1 = get_ctrl_group("Host parameters", 1, "m", *m_sliders[:IM["alpha"]])
pg2 = get_ctrl_group("Vector parameters", 2, "m", *m_sliders[IM["alpha"]:IM["nu_m"]])
pg3 = get_ctrl_group("Preference parameters", 3, "m", *m_sliders[IM["nu_m"]:IM["host-inc-0"]])
pg5 = get_ctrl_group("Initial conditions", 5, "m", *m_sliders[IM["host-inc-0"]:])

custom_params = html.Div(
        id="m-custom-params",
        className="invisible",
        children=[
    
            html.Span(className="emph-line"),
            
            html.H4("Custom parameters", className="uppercase-title"),

            m_PT_or_not,

            pg1,
            pg2,
            pg3,
            pg5,

        ])


model_controls = html.Div([

        html.Span(className="emph-line"),
        html.H4("Controls", className="uppercase-title"),

        param_choice,
        custom_params,
        
    ], className="controls")



col_no_selector = html.Div([
                html.P("Number of figure columns", className="control-label"),
                
                dcc.RadioItems(
                    id=f"col-choice",
                    options=[
                        {'label': ' One column ', 'value': 1},
                        {'label': ' Two columns ', 'value': 2},
                    ],
                    value=1,
                    labelStyle={'display': 'block'}
                ),
        
            ],
            )


modal = get_modal("m")

settings_modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("Settings"),
                    dbc.ModalBody(
                        col_no_selector
                        ),
                ],
                id="settings-modal",
                is_open=False,
            ),
        ],
        )



settings_logo = html.Div(
                html.Img(src='/assets/images/settings.svg',
                    id="settings-icon"),
                id="settings-wrapper",
                className="show-desktop"
                )



figs_and_tables = html.Div([
            #
                
                    html.Div([
                        html.Span(className="emph-line"),
                        html.H4("host dynamics", className="uppercase-title"),
                    

                    html.Div(dcc.Graph(id='host-fig',
                        config = MODEBAR_CONFIG,
                        className="fig-cont"
                        )),
                ]),
                
                #
                html.Div([
                    html.Span(className="emph-line"),
                    html.H4("vector dynamics", className="uppercase-title"),

                    html.Div(dcc.Graph(id='vector-fig',
                        config = MODEBAR_CONFIG,
                        className="fig-cont"
                        )),
                ]),

                #
                html.Div([

                    html.Span(className="emph-line"),
                    html.H4("incidence dynamics", className="uppercase-title"),

                    html.Div(dcc.Graph(id='incidence-fig',
                        config = MODEBAR_CONFIG,
                        className="fig-cont"
                        )),
                ]),

                #
                html.Div([

                    #
                    html.Span(className="emph-line"),
                    html.H4("Equilibria", className="uppercase-title"),
                    html.Div(id="eqm-table-cont", className="table-container"),
                    
                    #
                    html.Span(className="emph-line"),
                    html.H4("Model quantities", className="uppercase-title"),
                    html.Div(id="R0-k-table-cont", className="table-container"),
                    
                ]),


            ],
            id="model-fig-wrapper",
            className="one-col"
            )



figure_cont = html.Div([
            
            html.Div(dcc.Loading(
                    html.Div(id="loading-m"),
                    color='rgba(0,0,0,0)',
                    type="circle",
                    ),
                    id="grey-screen-wrapper-m"
                    ),

            html.Div(dbc.Spinner(
                    html.Div(id="loading-m-2"),
                    spinner_style={"width": "60px", "height": "60px", "font-size": "20px"},
                    color='#295939'),
                    className="fig-spinner"
                    ),

            settings_logo,
            
            figs_and_tables,

            ],
            className="figure-cont")




model_page =  html.Div(
    [
    modal,
    settings_modal,

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