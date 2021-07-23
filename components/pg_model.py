import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from utils.figures import MODEBAR_CONFIG
from components.helper_fns import slider_list, get_ctrl_group, get_sliders, \
    get_par_choice

m_sliders = get_sliders(slider_list, "")

m_PT_or_not = html.Div([
            
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




param_choice = get_par_choice("")


pg1 = get_ctrl_group("Host parameters", 1, "", *m_sliders[:3])
pg2 = get_ctrl_group("Vector parameters", 2, "", *m_sliders[3:10])
pg3 = get_ctrl_group("Preference parameters", 3, "", *m_sliders[10:16])
# pg4 = get_ctrl_group("Transmission parameters", 4, "", *m_sliders[16:18])
pg5 = get_ctrl_group("Initial conditions", 5, "", *m_sliders[16:])

custom_params = html.Div(
        id="custom-params",
        children=[
    
            html.Span(className="emph-line"),
            
            html.H4("Custom parameters", className="uppercase-title"),

            m_PT_or_not,

            pg1,
            pg2,
            pg3,
            # pg4,
            pg5,

        ])




model_controls = html.Div([

        html.Span(className="emph-line"),
        html.H4("Controls", className="uppercase-title"),

        param_choice,
        custom_params,
        
    ], className="controls")




figure_cont = html.Div([

            #
            html.Span(className="emph-line"),
            html.H4("host dynamics", className="uppercase-title"),

            html.Div(dbc.Spinner(
                    html.Div(id="loading-m"),
                    color='#295939'),
                    ),

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