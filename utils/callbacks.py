from components.pg_model import model_page
from components.pg_explan import explan_page
from components.pg_404 import page_404
from components.pg_par_scan import par_scan_page
from components.helper_fns import slider_list

from utils.fns_general import get_params

from utils.fns_model import get_soln,  get_host_fig, \
    get_vec_fig, get_inc_fig, EqmTable, \
    get_R0_kappa_table, get_init_cnds

from utils.fns_par_scan import ParScanData, get_ps_var_info, get_var_name_for_scan

from utils.figures import TerminalIncidenceFigure



def model_callback(*params):

    p = get_params(*params[:-4])

    if not p.vc.is_valid:
        return [True,
                p.vc.error_message,
                dict(data=[], layout={}),
                dict(data=[], layout={}),
                dict(data=[], layout={}),
                None,
                None,
                None,
                None,
                ]
    


    try:
        return run_model_callback(p, *params)
    except:
        return [True,
            "Error in generating solution - try another parameter set",
            dict(data=[], layout={}),
            dict(data=[], layout={}),
            dict(data=[], layout={}),
            None,
            None,
            None,
            None,
            ]



def run_model_callback(p, *params):
    def_or_cust = params[0]
    N = params[2]
    IC_pars = params[-4:]

    initial_conds = get_init_cnds(p, def_or_cust, N, *IC_pars)

    soln = get_soln(p, initial_conds)

    fig_host = get_host_fig(soln)
    
    fig_vec = get_vec_fig(soln)
    
    fig_incidence = get_inc_fig(soln)

    tbl_eqm = EqmTable(p).tab

    tbl_R0_k = get_R0_kappa_table(p)

    return [False,
            "",
            
            fig_host,
            fig_vec,
            fig_incidence,
            
            tbl_eqm,
            tbl_R0_k,

            None,
            None,
            ]




def par_scan_callback(button, *params):

    p = get_params(*params[:-2])

    if not p.vc.is_valid:
        return [True,
                p.vc.error_message,
                dict(data=[], layout={}),
                dict(data=[], layout={}),
                None,
                None,
                ]

    return run_PS_callback(*params)
    
    try:
        return run_PS_callback(*params)
    except:
        return [True,
            "Error in generating solution - try another parameter set",
            dict(data=[], layout={}),
            dict(data=[], layout={}),
            None,
            None,
            ]




def run_PS_callback(*params):

    var_use = get_var_name_for_scan(params[0], params[1], params[-2], params[-1])
    
    pars_use = list(params[:-2]) + [var_use]

    x_info = get_ps_var_info(slider_list, var_use)

    data = ParScanData(x_info, *pars_use).data

    host_fig = TerminalIncidenceFigure(data, x_info, "host").fig
    
    vec_fig = TerminalIncidenceFigure(data, x_info, "vec").fig

    return [False,
            "",
            host_fig, 
            vec_fig,
            None,
            None,
            ]




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



def make_sliders_invisible_m(trans_type):
    if trans_type=="NPT":
        return ["invisible"]*6 + ["control-wrapper"]*3
    elif trans_type=="PT":
        return ["control-wrapper"]*6 + ["invisible"]*3
    else:
        raise Exception(f"Transmission type invalid: {trans_type}")




def make_sliders_invisible_ps(default, persistent):
    NPT_config = ["invisible"]*6 + ["control-wrapper"]*3 + ["control-wrapper"] + ["invisible"]
    PT_config = ["control-wrapper"]*6 + ["invisible"]*3 + ["invisible"] + ["control-wrapper"]
    if default=="def-NPT":
        return NPT_config
    
    elif default=="def-PT":
        return PT_config
        
    elif default=="def-C":
        if persistent=="NPT":
            return NPT_config
        elif persistent=="PT":
            return PT_config
        else:
            raise Exception(f"transmission type (custom setting) invalid: {persistent}")
    else:
        raise Exception(f"Transmission type (main setting) invalid: {default}")
    