from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from components.header import header
from components.footer import footer
from components.pg_model import slider_list


from utils.utils import retrieve_page, model_callback, toggle_open, toggle_visible

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
        <meta name="Plant disease vector preference model" 
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
            [Input('page-url', 'pathname')]
            )(retrieve_page)


# toggle open/close menus and navs
ids = ["nav-menu"] + [f"sld-gp-{x}" for x in range(1,6)]
acts = ["menu-button"] + [f"sld-bt-{x}" for x in range(1,6)]

for id_name, activator in zip(ids,acts):
    app.callback(Output(id_name, "is_open"),
        [Input(activator, "n_clicks")],
        [State(id_name, "is_open")],
    )(toggle_open)


# run model
app.callback([
                Output("model-fig", "figure"),
                Output("model-fig-title", "children"),
            ],
            [Input('param-choice', 'value')]
            + [Input('persistent-choice', 'value')]
            + [Input(f"slider-{x['var']}", 'value') for x in slider_list]
            )(model_callback)

# make params invisible
app.callback([Output("custom-params", "className")],
    [Input('param-choice', 'value')],
    )(toggle_visible)




if __name__ == '__main__':
    # False for production, True for development
    # should use a .env file or similar really, so that this is always correct
    DEBUG = True

    app.run_server(debug=DEBUG)