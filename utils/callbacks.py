from components.pg_model import model_page
from components.pg_explan import explan_page
from components.pg_404 import page_404
from components.pg_par_scan import par_scan_page
from components.slr_list import SLIDER_LIST, SLIDER_IND_MAP

from utils.fns_general import get_params

from utils.fns_model import get_soln,  get_host_fig, \
    get_vec_fig, get_inc_fig, EqmTable, \
    get_R0_kappa_table, get_init_cnds

from utils.fns_par_scan import ParScanData, get_ps_var_info, get_var_name_for_scan

from utils.figures import TerminalIncidenceFigure


IM = SLIDER_IND_MAP


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

    except Exception as e:
        print(f"Model callback error: {e}")
        
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
                None,
                None,
                ]

    try:
        return run_PS_callback(*params)
    except Exception as e:
        print(f"PS callback error: {e}")

        return [True,
            "Error in generating solution - try another parameter set",
            dict(data=[], layout={}),
            None,
            None,
            ]




def run_PS_callback(*params):
    
    var_use = get_var_name_for_scan(def_or_custom=params[0],
                                    cust_choice=params[1],
                                    NPT_var=params[-2],
                                    PT_var=params[-1])
    

    x_info = get_ps_var_info(SLIDER_LIST, var_use)

    pars_use = list(params[:-2]) + [var_use]
    
    data = ParScanData(x_info, *pars_use).data

    host_fig = TerminalIncidenceFigure(data, x_info, "host").fig
    
    return [False,
            "",
            host_fig, 
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

def toggle_fig_columns(value):
    if value==2:
        return ["two-cols"]
    elif value==1:
        return ["one-col"]
    else:
        print(f"value should be 1 or 2 but received: {value}")
        return ["one-col"]


def make_sliders_invisible_m(trans_type):
    inv = ["invisible"]
    cw = ["control-wrapper"]
    
    NPT_config = cw + inv + cw + inv + inv*6 + cw*3
    PT_config = inv + cw + inv + cw + cw*6 + inv*3

    if trans_type=="NPT":
        return NPT_config

    elif trans_type=="PT":
        return PT_config

    else:
        raise Exception(f"Transmission type invalid: {trans_type}")




def make_sliders_invisible_ps(default, persistent):
    inv = ["invisible"]
    cw = ["control-wrapper"]

    NPT_config = cw + inv + cw + inv + inv*6 + cw*3 + cw + inv
    PT_config = inv + cw + inv + cw + cw*6 + inv*3 + inv + cw

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
    