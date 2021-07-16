from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate

# from gevent.pywsgi import WSGIServer
# from flask import Flask

from components.header import header
from components.footer import footer

from utils.utils import retrieve_page, model_callback, toggle_open

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
# edit meta below so search engines can find
# add analytics into head
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <meta name="Vector Paper" 
        content="Mathemtical model of vector/host interactions">

        {%metas%}
        <title>Vector Paper</title>
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
            [Input('page-url', 'pathname')])(retrieve_page)


# toggle open/close menus and navs
for id_name, activator in zip(["nav-menu"],
                                ["menu-button"]):

    app.callback(Output(id_name, "is_open"),
        [Input(activator, "n_clicks")],
        [State(id_name, "is_open")],
    )(toggle_open)


# run model
app.callback([
                Output("model-fig", "figure"),
                Output("model-fig-title", "children"),
            ],
            [
                Input('checklist', 'value'),
                Input('slider', 'value'),
            ]
            )(model_callback)

########################################################################################################################
if __name__ == '__main__':
    # False for production, True for development
    # should use a .env file or similar really, so that this is always correct
    DEBUG = True

    app.run_server(debug=DEBUG)