import dash_table
import pandas as pd
import numpy as np

from utils.figures import model_fig, get_traces, get_traces_scan_fig

from model.pars import DefaultParams, CustomParams
from model.eqm_fns import RootAnalyser, StabilityMatrix
from model.simulator import Simulator

def get_soln(p, itl_cnds):
        
    sim = Simulator(p, itl_cnds)
    sim.run()

    return sim.out



def get_host_fig(soln):

    xs = [soln.t, soln.t]
    ys = [soln.S, soln.I]
    clrs = ["#00b050", "#c00000"]
    names = ["Susceptible: S", "Infected: I"]

    trcs = get_traces(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Number of hosts", True)
    
    return fig



def get_vec_fig(soln):
    
    xs = [soln.t, soln.t]
    ys = [soln.X, soln.Z]
    clrs = ["#92d050", "#e46c0a"]
    names = ["Nonviruliferous: X", "Viruliferous: Z"]
    
    trcs = get_traces(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Number of vectors", True)
    
    return fig


def get_inc_fig(soln):
    
    xs = [soln.t, soln.t]
    
    y1 = [(soln.I[ii])/(soln.I[ii] + soln.S[ii]) for ii in range(len(soln.S))]
    y2 = [(soln.Z[ii])/(soln.Z[ii] + soln.X[ii]) for ii in range(len(soln.X))]
    
    ys = [y1, y2]

    clrs = ["rgb(255,202,211)", "rgb(151,11,238)"]

    names = ["Host incidence: I/(S+I)", "Vector incidence: Z/(X+Z)"]

    trcs = get_traces(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Incidence", True)
    
    return fig




def get_eqm_table(p):
    rta = RootAnalyser(p)
    
    df = rta.df

    df = df[df['bio_realistic']]

    df = df.round(3)

    df = df.drop(columns=["solves_system", "tol", "bio_realistic"])

    df.columns = list(df.columns[:-1]) + ["Stable?"]

    return my_table(df)



def get_x_min_and_max(slider_list, var):
    df = pd.DataFrame(slider_list)
    filtered = df[df["var"]==var]

    xmin = list(filtered["min"])[0]
    xmax = list(filtered["max"])[0]
    return xmin, xmax




def get_ps_equilibria_df(p, var, xmin, xmax):
    
    xs = []
    ys = []
    stabs = []
    
    for x in np.linspace(xmin, xmax, 501):
        setattr(p, var, x)

        try:
            y, stab = get_terminal_incidence_and_stab(p)
            ys += y
            xs += [x]*len(y)
            stabs += stab
        except Exception as e:
            print("nt error", e)

            xs += [x]
            ys += [None]
            stabs += [None]
    
    return pd.DataFrame(dict(x=xs, y=ys, stab=stabs))


def get_eqm_vals(p):
    rta = RootAnalyser(p)
    
    df = rta.df

    df = df[df['bio_realistic']]

    df = df.round(3)

    df = df.drop(columns=["solves_system", "tol", "bio_realistic"])    

    return df


def get_dis_free_df(p, xmin, xmax, var):
    kappa = get_kappa(p)
    
    xs = []
    ys = []
    stabs = []

    for x in np.linspace(xmin, xmax, 501):
        setattr(p, var, x)
        dis_free_eqm = [p.N, 0, kappa, 0]
        stab = check_stability_dis_free(p, dis_free_eqm)
        xs.append(x)
        ys.append(0)
        stabs.append(stab)

    return pd.DataFrame(dict(x=xs, y=ys, stab=stabs))



def check_stability_dis_free(p, vec):
    stab = StabilityMatrix(p, vec)
    return stab.is_stable
    


def get_R0_kappa_table(p):

    kappa = get_kappa(p)
    R0 = get_R0(p, kappa)

    data = dict(R0=[R0], kappa=[kappa])
    
    df = pd.DataFrame(data)

    return my_table(df)




def get_kappa(p):
    mult = (p.alpha/p.sigma)
    inner_bracket = (1/p.om_m) - 1
    bracket = 1+ p.delta * inner_bracket
    out = p.zeta * (1 - mult * bracket)
    return out



def get_R0(p, kappa):
    R_PV = get_RPV(p, kappa)
    R_VP = get_RVP(p)

    out = (R_PV * R_VP)**(0.5)
    return out

def get_RPV(p, kappa):
    num = kappa * p.eta * p.nu_m
    denom = p.N * p.om_m * p.Gamma * (p.mu + p.rho)
    out = num/denom
    return out

def get_RVP(p):
    inn2_brack = (1/p.om_p) - 1
    inner_brack = 1 + p.delta * inn2_brack
    bracket = p.tau + p.alpha * inner_brack
    denom = p.om_p * p.Gamma * bracket
    out = p.gamma/denom
    return out






def my_table(df):
    return dash_table.DataTable(
        data = df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        
        style_as_list_view=True,

        style_cell = {
                'font-family': 'sans-serif',
                'padding': '5px 20px',
                'font_size': '12px',
            },
        
        fill_width=False,
        )



def get_params(*params):
    if params[0]=="def-NPT":
        return DefaultParams("NPT")
    elif params[0]=="def-PT":
        return DefaultParams("PT")
    elif params[0]=="def-C":
        return CustomParams(*params[1:])
    else:
        raise Exception("invalid transmission type entered")



def get_init_cnds(p, *params):
    kappa = get_kappa(p)
    if params[0]=="def-NPT":
        return [999, 1, kappa-1, 1]
    elif params[0]=="def-PT":
        return [999, 1, kappa-1, 1]
    elif params[0]=="def-C":
        out = get_custom_init_conds(kappa, *params)
        return out
    else:
        raise Exception("invalid transmission type entered")



def get_custom_init_conds(kappa, *params):
    
    N = params[2]

    host_inc = params[-4]
    host_prop = params[-3]
    vec_inc = params[-2]
    vec_prop = params[-1]

    S0 = N * host_prop * (1-host_inc)
    I0 = N * host_prop * host_inc
    
    X0 = kappa * vec_prop * (1-vec_inc)
    Z0 = kappa * vec_prop * vec_inc

    return [S0, I0, X0, Z0]


def get_terminal_incidence_and_stab(p):
    df = get_eqm_vals(p)

    I_list = list(df.I)
    S_list = list(df.S)

    term_inc = [I_list[ii]/(S_list[ii] + I_list[ii]) for ii in range(len(S_list))]
    stability = list(df.is_stable)

    return term_inc, stability


def get_scan_fig(xs, ys, var, stab):

    clrs = ["rgb(0,89,0)" if ss else "rgb(151,251,151)" for ss in stab]
    names = ["Stable" if ss else "Unstable" for ss in stab]

    showledge = get_showlegend(xs)
    
    trcs = get_traces_scan_fig(xs, ys, clrs, names, showledge)

    fig = model_fig(trcs, var, u"Terminal incidence: I/(S+I) at t=\u221E", True)
    return fig


def get_showlegend(xs):
    
    showledge = [False, False, True, True]

    # if one of traces are empty, use other option to fill legend
    if not xs[2]:
        showledge[0] = True
    if not xs[3]:
        showledge[1] = True

    return showledge