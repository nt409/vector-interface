import dash_table
import pandas as pd

from utils.figures import model_fig, get_traces

from model.pars import DefaultParams, CustomParams
from model.eqm_fns import RootAnalyser
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
    fig = model_fig(trcs, "Time (days)", "Number of hosts")
    
    return fig



def get_vec_fig(soln):
    # todo
    xs = [soln.t, soln.t]
    ys = [soln.X, soln.Z]
    clrs = ["#92d050", "#e46c0a"]
    names = ["Nonviruliferous: X", "Viruliferous: Z"]
    
    trcs = get_traces(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Number of vectors")
    
    return fig


def get_inc_fig(soln):
    # todo
    xs = [soln.t, soln.t]
    
    y1 = [(soln.I[ii])/(soln.I[ii] + soln.S[ii]) for ii in range(len(soln.S))]
    y2 = [(soln.Z[ii])/(soln.Z[ii] + soln.X[ii]) for ii in range(len(soln.X))]
    
    ys = [y1, y2]

    clrs = ["rgb(255,202,211)", "rgb(151,11,238)"]

    names = ["Host incidence: I/(S+I)", "Vector incidence: Z/(X+Z)"]

    trcs = get_traces(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Incidence")
    
    return fig




def get_eqm_table(p):
    rta = RootAnalyser(p)
    
    df = rta.df

    df = df[df['bio_realistic']]

    df = df.round(3)

    df = df.drop(columns=["solves_system", "tol", "bio_realistic"])

    df.columns = list(df.columns[:-1]) + ["Stable?"]

    return my_table(df)




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