import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from utils.figures import MODEBAR_CONFIG

from components.slr_list import slider_list, SLIDER_IND_MAP
from components.helper_fns import get_run_button, get_ctrl_group, get_sliders, \
    get_par_choice, get_modal, get_dropdown, get_scenario_radio

ps_sliders = get_sliders(slider_list, "ps")


IM = SLIDER_IND_MAP

NPT_dd_vars = (slider_list[:IM["tau-NPT"]] 
    + [slider_list[IM["tau-NPT"]],
        slider_list[IM["sigma"]],
        slider_list[IM["zeta-NPT"]]] 
    + slider_list[IM["Gamma"]:IM["nu_m"]]
    + slider_list[IM["nu"]:IM["host-inc-0"]])

PT_dd_vars =  (slider_list[:IM["tau-NPT"]] 
    + [slider_list[IM["tau-PT"]],
        slider_list[IM["sigma"]],
        slider_list[IM["zeta-PT"]]] 
    + slider_list[IM["Gamma"]:IM["host-inc-0"]])

ps_which_var_NPT = get_dropdown("NPT", NPT_dd_vars, "control-wrapper")
ps_which_var_PT = get_dropdown("PT", PT_dd_vars, "invisible")

ps_PT_or_not = get_scenario_radio("ps")

pg1 = get_ctrl_group("Host parameters", 1, "ps", *ps_sliders[:IM["alpha"]])
pg2 = get_ctrl_group("Vector parameters", 2, "ps", *ps_sliders[IM["alpha"]:IM["nu_m"]])
pg3 = get_ctrl_group("Preference parameters", 3, "ps", *ps_sliders[IM["nu_m"]:IM["host-inc-0"]])

cust_params = html.Div(
        id="ps-custom-params",
        className="invisible",
        children=[
    
            html.Span(className="emph-line"),
            html.H4("Custom parameters", className="uppercase-title"),

            ps_PT_or_not,

            pg1,
            pg2,
            pg3,
        ])

param_choice = get_par_choice("ps")

plot_button = get_run_button("ps")



ps_controls = html.Div([

        html.Span(className="emph-line"),

        html.H4("Controls", className="uppercase-title"),

        ps_which_var_NPT,
        
        ps_which_var_PT,

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