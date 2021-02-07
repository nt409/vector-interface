from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate

from gevent.pywsgi import WSGIServer

from flask import Flask


from header import header
from footer import footer


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
        <meta name="MyWebsiteName" 
        content="Something about what my website does">

        {%metas%}
        <title>MyWebsiteName</title>
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

@app.callback(Output('page-content', 'children'),
            [Input('page-url', 'pathname')])
def display_page(pathname):
    if pathname == '/model':
        return html.Div("model")
    elif pathname == '/':
        return html.Div("home")
    else:
        return html.Div('404: Page not found',style={'height': '100vh'})


# collapse
def toggle(n, is_open):
    if n:
        return not is_open
    return is_open



########################################################################################################################
for id_name, activator in zip(["nav-menu"],
                                ["menu-button"]):

    app.callback(Output(id_name, "is_open"),
        [Input(activator, "n_clicks")
        ],
        [State(id_name, "is_open")],
    )(toggle)


########################################################################################################################
if __name__ == '__main__':
    # False for production, True for development
    # should use a .env file or similar really, so that this is always correct
    WILL_DEBUG = True

    app.run_server(debug=WILL_DEBUG)