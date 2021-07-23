import pandas as pd

from components.pg_model import model_page
from components.pg_explan import explan_page
from components.pg_404 import page_404
from components.pg_par_scan import par_scan_page
from components.helper_fns import slider_list

from utils.fns import get_soln, get_params, get_host_fig, \
    get_vec_fig, get_inc_fig, get_eqm_table, \
    get_R0_kappa_table, get_init_cnds, get_scan_fig, \
    get_x_min_and_max, get_ps_equilibria_df, \
    get_dis_free_df




def model_callback(*params):
    p = get_params(*params)

    initial_conds = get_init_cnds(p, *params)

    soln = get_soln(p, initial_conds)

    fig_host = get_host_fig(soln)
    
    fig_vec = get_vec_fig(soln)
    
    fig_incidence = get_inc_fig(soln)

    tbl_eqm = get_eqm_table(p)

    tbl_R0_k = get_R0_kappa_table(p)

    return [fig_host, fig_vec, fig_incidence, tbl_eqm, tbl_R0_k, None]




def par_scan_callback(*params):
    p = get_params(*params)

    var = params[-1]

    xmin, xmax = get_x_min_and_max(slider_list, var)

    df_out = get_ps_equilibria_df(p, var, xmin, xmax)

    df_s = df_out[df_out["stab"].isin([True, None])]
    df_u = df_out[df_out["stab"].isin([False, None])]    

    p = get_params(*params)
    df = get_dis_free_df(p, xmin, xmax, var)
    
    dis_free_s = df[df["stab"].isin([True])]
    dis_free_u = df[df["stab"].isin([False])]
    
    xs_plot = [list(dis_free_s.x), list(dis_free_u.x), list(df_s.x), list(df_u.x)]
    ys_plot = [list(dis_free_s.y), list(dis_free_u.y), list(df_s.y), list(df_u.y)]
    stabs_plot = [True, False, True, False]

    scan_figr = get_scan_fig(xs_plot, ys_plot, var, stabs_plot)

    return [scan_figr, None]




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

