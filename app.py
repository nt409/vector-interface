from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from components.header import header
from components.footer import footer
from components.helper_fns import slider_list


from utils.callbacks import retrieve_page, model_callback, toggle_open, toggle_visible, \
    par_scan_callback, toggle_modal

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

        ],
        )


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
ids = ["nav-menu"] + [f"sld-gp-{x}" for x in range(1,6)] + [f"ps-sld-gp-{x}" for x in range(1,6)]
acts = ["menu-button"] + [f"sld-bt-{x}" for x in range(1,6)] + [f"ps-sld-bt-{x}" for x in range(1,6)]

for id_name, activator in zip(ids,acts):
    app.callback(Output(id_name, "is_open"),
        [Input(activator, "n_clicks")],
        [State(id_name, "is_open")],
    )(toggle_open)



# make params invisible
ids = ["custom-params", "ps-custom-params"]
acts = ["param-choice", "ps-param-choice"]

for id_name, activator in zip(ids, acts):
    app.callback([Output(id_name, "className")],
        [Input(activator, "value")],
        )(toggle_visible)


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
            [Input('param-choice', 'value')]
            + [Input('persistent-choice', 'value')]
            + [Input(f"slider-{x['var']}", 'value') for x in slider_list]
            )(model_callback)

# run par scan
app.callback([
              Output("ps-error-modal", "is_open"),
              Output("ps-modal-content", "children"),
              Output("ps-host-fig", "figure"),
              Output("ps-vec-fig", "figure"),
              Output("loading-ps", "children"),
              Output("loading-ps-2", "children"),
              ],
            [Input('ps-run-button', 'n_clicks')],
            [State('ps-param-choice', 'value')]
            + [State('ps-persistent-choice', 'value')]
            + [State(f"ps-slider-{x['var']}", 'value') for x in slider_list[:-4]]
            + [State('ps-variable-choice', 'value')]
            )(par_scan_callback)






if __name__ == '__main__':
    # False for production, True for development
    # should use a .env file or similar really, so that this is always correct
    DEBUG = True

    app.run_server(debug=DEBUG)