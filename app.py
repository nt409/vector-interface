from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from components.header import header
from components.footer import footer
from components.slr_list import SLIDER_IND_MAP, SLIDER_LIST


from utils.callbacks import retrieve_page, model_callback, toggle_open, toggle_visible, \
    par_scan_callback, make_sliders_invisible_m, make_sliders_invisible_ps

########################################################################################################################
external_stylesheets = [dbc.themes.LITERA]

app = Dash(__name__, 
        external_stylesheets=external_stylesheets,
        assets_folder='assets')

server = app.server

app.config.suppress_callback_exceptions = True

########################################################################################################################

app.layout = html.Div([

        header,

        dcc.Location(id='page-url', refresh=False),
        
        html.Div(id='page-content', children=html.Div('Loading...'), className="wrapper"),

        footer,

        ])


########################################################################################################################
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <meta name="Plant disease vector preference model" 
        content="Mathemtical model of vector/host interactions">

        {%metas%}
        <title>Plant disease vector preference model</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Google+Sans">
        <link rel="icon" href="assets/favicon.ico">
        {%css%}
        
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


########################################################################################################################
# callbacks

# display page depending on url
app.callback(Output('page-content', 'children'),
            [Input('page-url', 'pathname')]
            )(retrieve_page)


# toggle open/close menus and navs
ids = ["nav-menu"] + [f"m-sld-gp-{x}" for x in range(1,6)] + [f"ps-sld-gp-{x}" for x in range(1,6)]
acts = ["menu-button"] + [f"m-sld-bt-{x}" for x in range(1,6)] + [f"ps-sld-bt-{x}" for x in range(1,6)]

for id_name, activator in zip(ids,acts):
    app.callback(Output(id_name, "is_open"),
        [Input(activator, "n_clicks")],
        [State(id_name, "is_open")],
    )(toggle_open)


# make params invisible
ids = ["m-custom-params", "ps-custom-params"]
acts = ["m-param-choice", "ps-param-choice"]

for id_name, activator in zip(ids, acts):
    app.callback([Output(id_name, "className")],
        [Input(activator, "value")],
        )(toggle_visible)

IM = SLIDER_IND_MAP

# make nu/om/eps sliders invisible depending on NPT vs PT, also variable dropdown
app.callback(
    [Output(f"ps-slider-comp-wrapper-{x['var']}", 'className') for x in SLIDER_LIST[IM["tau-NPT"]:IM["sigma"]]] +
    [Output(f"ps-slider-comp-wrapper-{x['var']}", 'className') for x in SLIDER_LIST[IM["zeta-NPT"]:IM["Gamma"]]] +
    [Output(f"ps-slider-comp-wrapper-{x['var']}", 'className') for x in SLIDER_LIST[IM["nu_m"]:IM["host-inc-0"]]] +
    [Output(f"ps-var-choice-wrapper-{suffix}", 'className') for suffix in ["NPT", "PT"]],
    [Input(f"ps-param-choice", 'value'),
    Input(f"ps-persistent-choice", 'value'),
    ]
    )(make_sliders_invisible_ps)


# make nu/om/eps sliders invisible depending on NPT vs PT
app.callback(
            [Output(f"m-slider-comp-wrapper-{x['var']}", 'className') for x in SLIDER_LIST[IM["tau-NPT"]:IM["sigma"]]] +
            [Output(f"m-slider-comp-wrapper-{x['var']}", 'className') for x in SLIDER_LIST[IM["zeta-NPT"]:IM["Gamma"]]] +
            [Output(f"m-slider-comp-wrapper-{x['var']}", 'className') for x in SLIDER_LIST[IM["nu_m"]:IM["host-inc-0"]]]
            ,
            [Input(f"m-persistent-choice", 'value')]
            )(make_sliders_invisible_m)


# run model
app.callback([
              Output("m-error-modal", "is_open"),
              Output("m-modal-content", "children"),
              Output("host-fig", "figure"),
              Output("vector-fig", "figure"),
              Output("incidence-fig", "figure"),
              Output("eqm-table-cont", "children"),
              Output("R0-k-table-cont", "children"),
              Output("loading-m", "children"),
              Output("loading-m-2", "children"),
            ],
            [Input('m-param-choice', 'value')]
            + [Input('m-persistent-choice', 'value')]
            + [Input(f"m-slider-{x['var']}", 'value') for x in SLIDER_LIST]
            )(model_callback)


# run par scan
app.callback([
              Output("ps-error-modal", "is_open"),
              Output("ps-modal-content", "children"),
              Output("ps-host-fig", "figure"),
              Output("loading-ps", "children"),
              Output("loading-ps-2", "children"),
              ],
            [Input('ps-run-button', 'n_clicks')],
            [State('ps-param-choice', 'value')]
            + [State('ps-persistent-choice', 'value')]
            + [State(f"ps-slider-{x['var']}", 'value') for x in SLIDER_LIST[:-4]]
            + [State('ps-variable-choice-NPT', 'value')]
            + [State('ps-variable-choice-PT', 'value')]
            )(par_scan_callback)






if __name__ == '__main__':
    # False for production, True for development
    # should use a .env file or similar really, so that this is always correct
    DEBUG = True

    app.run_server(debug=DEBUG)