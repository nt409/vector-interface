# callbacks and model fns

from components.pg_model import model_page
from components.pg_explan import explan_page
from components.pg_404 import page_404

from utils.figures import model_fig



def retrieve_page(pathname):
    if pathname == '/':
        return model_page
    elif pathname == '/explanation':
        return explan_page
    else:
        return page_404


def toggle_open(n, is_open):
    if n:
        return not is_open
    return is_open


def toggle_visible(radio):
    if radio=="C":
        return [""]
    else:
        return ["invisible"]



def model_callback(*params):
    
    radio = params[0]
    slider = params[2]

    print(params)
    
    x = [1]
    y = [1]
    
    clr = "black"
    
    fig = model_fig(x, y, clr, slider)
    
    title =f"Figure title"
    
    return [fig, title]