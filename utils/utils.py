# add some functions if you have a model that calculates something!

from components.pg_model import model_page
from components.pg_explan import explan_page
from components.pg_404 import page_404

from utils.figures import model_fig



def retrieve_page(pathname):
    if pathname == '/explanation':
        return explan_page
    elif pathname == '/':
        return model_page
    else:
        return page_404


def toggle_open(n, is_open):
    if n:
        return not is_open
    return is_open


def model_callback(*params):
    print(params)
    
    slider = 8
    checklist = []
    
    x = [1]
    y = [1]
    
    if "in-red" in checklist:
        clr = "red"
    else:
        clr = "black"
    
    fig = model_fig(x, y, clr, slider)
    
    title =f"Figure title"
    
    return [fig, title]