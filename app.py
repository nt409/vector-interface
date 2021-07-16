from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate

from gevent.pywsgi import WSGIServer

from flask import Flask


from components.header import header
from components.footer import footer

from components.page_home import home_page
from components.page_model import model_page
from components.page_data import data_page
from components.page_not_found import page_404

from utils.figures import model_fig

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

@app.callback(Output('page-content', 'children'),
            [Input('page-url', 'pathname')])
def display_page(pathname):
    # if pathname == '/':
        # return model_page
    if pathname == '/explanation':
        return data_page
    elif pathname == '/':
        return model_page
    else:
        return page_404


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




@app.callback([
                Output("model-fig", "figure"),
                Output("model-fig-title", "children"),
            ],
            [
                Input('date-picker', 'date'),
                Input('checklist', 'value'),
                Input('slider', 'value'),
            ])
def model_callback(params, checklist, slider):
    
    x = [1]
    y = [1]
    
    if "in-red" in checklist:
        clr = "red"
    else:
        clr = "black"
    
    fig = model_fig(x, y, clr, slider)
    
    if "contains-date" in checklist:
        title =f"ylab on {str(params)}"
    else:
        title =f"ylab"
    
    return [fig, title]

########################################################################################################################
if __name__ == '__main__':
    # False for production, True for development
    # should use a .env file or similar really, so that this is always correct
    DEBUG = True

    app.run_server(debug=DEBUG)