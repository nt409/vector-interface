import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from utils.figures import MODEBAR_CONFIG
from components.helper_fns import get_run_button, slider_list, get_ctrl_group, get_sliders, \
    get_par_choice, get_modal


ps_sliders = get_sliders(slider_list, "ps-")

ps_which_var = html.Div([
            
            html.P("Variable choice", className="control-label"),
                
            dcc.Dropdown(
                            id="ps-variable-choice",
                            options=[
                                {'label': var["name"], 'value': var["var"]} 
                                for var in slider_list[:-4]
                            ],
                            value='mu',
                            clearable = False,
                            searchable=False,
                            optionHeight=60,
                        )
        
            ],
            className="control-wrapper"
            )

ps_PT_or_not = html.Div([
            
            html.P("Scenario", className="control-label"),
                
            dcc.RadioItems(
                            id="ps-persistent-choice",
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



pg1 = get_ctrl_group("Host parameters", 1, "ps-", *ps_sliders[:3])
pg2 = get_ctrl_group("Vector parameters", 2, "ps-", *ps_sliders[3:10])
pg3 = get_ctrl_group("Preference parameters", 3, "ps-", *ps_sliders[10:16])

cust_params = html.Div(
        id="ps-custom-params",
        children=[
    
            html.Span(className="emph-line"),
            html.H4("Custom parameters", className="uppercase-title"),

            ps_PT_or_not,

            pg1,
            pg2,
            pg3,
        ])

param_choice = get_par_choice("ps-")

plot_button = get_run_button("ps")



ps_controls = html.Div([

        html.Span(className="emph-line"),

        html.H4("Controls", className="uppercase-title"),

        ps_which_var,

        param_choice,

        cust_params,

        plot_button,
        
    ], className="controls")




figr_cont = html.Div([

            html.Div(dcc.Loading(
                    html.Div(id="loading-ps"),
                    color='rgba(0,0,0,0)',
                    type="circle",
                    ),
                    id="grey-screen-wrapper-ps"
                    ),

            html.Div(dbc.Spinner(
                    html.Div(id="loading-ps-2"),
                    spinner_style={"width": "60px", "height": "60px", "font-size": "20px"},
                    color='#295939'),
                    className="fig-spinner"
                    ),


            #
            html.Span(className="emph-line"),
            html.H4("parameter scan: terminal host incidence", className="uppercase-title"),
            

            html.Div(dcc.Graph(id='ps-host-fig',
                config = MODEBAR_CONFIG,
                className="fig-cont"
                )),
            
            #
            html.Span(className="emph-line"),
            html.H4("parameter scan: terminal vector incidence", className="uppercase-title"),
            

            html.Div(dcc.Graph(id='ps-vec-fig',
                config = MODEBAR_CONFIG,
                className="fig-cont"
                )),
            
            ],
            className="figure-cont sticky-desktop")


modal = get_modal("ps")


par_scan_page =  html.Div(
    [

    modal,
    
    html.H1(
        "Parameter scan",
        className="page-title"),
    
    html.Div([
        ps_controls,
        figr_cont,
        ],
        className="model-page"),
    
    ],
    className="page-contents")