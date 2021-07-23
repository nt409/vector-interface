# callbacks and model fns

from components.pg_model import model_page
from components.pg_explan import explan_page
from components.pg_404 import page_404
from components.pg_par_scan import par_scan_page

from utils.fns import get_soln, get_params, \
    get_host_fig, get_vec_fig, get_inc_fig, \
    get_eqm_table, get_R0_kappa_table, \
    get_init_cnds




def model_callback(*params):
    p = get_params(*params)

    initial_conds = get_init_cnds(p, *params)

    soln = get_soln(p, initial_conds)

    fig_host = get_host_fig(soln)
    
    fig_vec = get_vec_fig(soln)
    
    fig_incidence = get_inc_fig(soln)

    tbl_eqm = get_eqm_table(p)

    tbl_R0_k = get_R0_kappa_table(p)

    return [fig_host, fig_vec, fig_incidence, tbl_eqm, tbl_R0_k]




def retrieve_page(pathname):
    if pathname == '/':
        return model_page
    elif pathname == '/explanation':
        return explan_page
    elif pathname == '/param-scan':
        return par_scan_page
    else:
        return page_404


def toggle_open(n, is_open):
    if n:
        return not is_open
    return is_open


def toggle_visible(radio):
    if radio=="def-C":
        return [""]
    else:
        return ["invisible"]

