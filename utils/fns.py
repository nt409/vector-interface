import dash_table
import pandas as pd
import numpy as np

from utils.figures import model_fig, get_traces_clr_nm, get_term_inc_fig

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

    trcs = get_traces_clr_nm(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Number of hosts", True)
    
    return fig



def get_vec_fig(soln):
    
    xs = [soln.t, soln.t]
    ys = [soln.X, soln.Z]
    clrs = ["#92d050", "#e46c0a"]
    names = ["Nonviruliferous: X", "Viruliferous: Z"]
    
    trcs = get_traces_clr_nm(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Number of vectors", True)
    
    return fig


def get_inc_fig(soln):
    
    xs = [soln.t, soln.t]
    
    y1 = [(soln.I[ii])/(soln.I[ii] + soln.S[ii]) for ii in range(len(soln.S))]
    y2 = [(soln.Z[ii])/(soln.Z[ii] + soln.X[ii]) for ii in range(len(soln.X))]
    
    ys = [y1, y2]

    clrs = ["rgb(255,202,211)", "rgb(151,11,238)"]

    names = ["Host incidence: I/(S+I)", "Vector incidence: Z/(X+Z)"]

    trcs = get_traces_clr_nm(xs, ys, clrs, names)
    fig = model_fig(trcs, "Time (days)", "Incidence", True)
    
    return fig




def get_eqm_table(p):
    rta = RootAnalyser(p)
    
    df = rta.df

    df = df[df['bio_realistic']]

    df = df.drop(columns=["solves_system", "tol", "bio_realistic"])

    dis_f_eqm = get_dis_free_eqm_dict(p)
    
    df = df.append(dis_f_eqm, ignore_index=True)

    df = df.round(3)

    for ind in ["S", "I", "X", "Z", "host_inc", "vec_inc"]:
        df[ind] = df[ind].astype(float)

    df.columns = list(df.columns[:-3]) + ["Host incidence", "Vector incidence", "Stable?"]

    return my_table(df)



def get_dis_free_eqm_dict(p):

    kappa = get_kappa(p)
    
    dis_free_eqm = [p.N, 0, kappa, 0]
    
    stab = check_stability_of_eqm(p, dis_free_eqm)

    return dict(S=p.N,
            I=0,
            X=kappa,
            Z=0,
            host_inc=0,
            vec_inc=0,
            is_stable=stab,
            )

def get_trivial_eqm_dict(p):

    triv_eqm = [0, 0, 0, 0]

    stab = check_stability_of_eqm(p, triv_eqm)

    return dict(S=0,
            I=0,
            X=0,
            Z=0,
            host_inc="NA",
            vec_inc="NA",
            is_stable=stab,
            )


def get_x_min_max_lab(slider_list, var):
    df = pd.DataFrame(slider_list)
    filtered = df[df["var"]==var]

    xmin = list(filtered["min"])[0]
    xmax = list(filtered["max"])[0]
    xlab = list(filtered["axis_label"])[0]
    
    xval = list(filtered["value"])[0]

    if xval>0:
        high = 100*xmax/xval
        low = 100*xmin/xval
    else:
        high = "NA"
        low = "NA"

    out = dict(min=xmin, max=xmax, value=xval, lab=xlab, high=high, low=low)
    return out


def get_scan_figure(p, var, x_info, which_inc, *params):
    
    df_out = get_ps_equilibria_df(p, var, x_info, which_inc)

    df_s = df_out[df_out["stab"].isin([True, None])]
    df_u = df_out[df_out["stab"].isin([False, None])]    

    p = get_params(*params)

    dis_free = get_dis_free_df(p, var, x_info)
    
    dis_free_s = dis_free[dis_free["stab"].isin([True])]
    dis_free_u = dis_free[dis_free["stab"].isin([False])]

    # # get "non-gap" background lines
    # df_srtd = df_out.sort_values(by=["y", "x"])
    # df_srtd = df_srtd[~df_srtd["stab"].isin([None])]

    # x_join, y_join = get_joiner_0_to_non_0(df_srtd)

    # x_non_0, y_non_0 = get_joiner_non_0(df_srtd)
    

    xs_plot = [
                # x_join,
                # x_non_0,
                # list(dis_free.x),
                list(dis_free_s.x),
                list(dis_free_u.x),
                list(df_s.x),
                list(df_u.x)]
    
    ys_plot = [
                # y_join,
                # y_non_0,
                # list(dis_free.y),
                list(dis_free_s.y),
                list(dis_free_u.y),
                list(df_s.y),
                list(df_u.y)]
    
    stabs_plot = [
                # None,
                # None,
                # None,
                True,
                False,
                True,
                False]

    y_str = "I/(S+I)" if which_inc=="host" else "Z/(X+Z)"

    fig = get_term_inc_fig(xs_plot, ys_plot, stabs_plot, x_info, y_str)

    return fig



def get_joiner_non_0(df_srtd):
    
    y_use = list(df_srtd.y)
    
    y_diffs = [abs(y_use[ii+1] - y_use[ii])
                    for ii in range(len(y_use)-1)]
    
    if max(y_diffs)>max(y_use)/50:
        x_non_0 = []
        y_non_0 = []
    else:
        x_non_0 = list(df_srtd.x)
        y_non_0 = list(df_srtd.y)

    return x_non_0, y_non_0


def get_joiner_0_to_non_0(df_srtd):
    y_use = list(df_srtd.y)

    if min(y_use)<max(y_use)/50:
        x1 = list(df_srtd.x)[0]
        x2 = list(df_srtd.x)[0]
        
        x_join = [x1, x2]
        y_join = [0, list(df_srtd.y)[0]]
    else:
        x_join = []
        y_join = []
    return x_join, y_join


def get_ps_equilibria_df(p, var, x_info, which_inc):
    
    xs = []
    ys = []
    stabs = []
    
    for x in np.linspace(x_info["min"], x_info["max"], 501):
        setattr(p, var, x)

        try:
            y, stab = get_terminal_incidence_and_stab(p, which_inc)
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

    return df


def get_dis_free_df(p, var, x_info):
    kappa = get_kappa(p)
    
    xs = []
    ys = []
    stabs = []

    for x in np.linspace(x_info["min"], x_info["max"], 501):
        setattr(p, var, x)
        dis_free_eqm = [p.N, 0, kappa, 0]
        stab = check_stability_of_eqm(p, dis_free_eqm)
        xs.append(x)
        ys.append(0)
        stabs.append(stab)

    return pd.DataFrame(dict(x=xs, y=ys, stab=stabs))



def check_stability_of_eqm(p, vec):
    stab = StabilityMatrix(p, vec)
    return stab.is_stable
    


def get_R0_kappa_table(p):

    kappa = get_kappa(p)
    R0 = get_R0(p, kappa)

    data = dict(R0=[R0], kappa=[kappa])
    
    df = pd.DataFrame(data)

    df = df.round(3)

    return my_table(df)




def get_kappa(p):
    mult = (p.alpha/p.sigma)
    inner_bracket = (1/p.om_m) - 1
    bracket = 1 + p.delta * inner_bracket
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
                'padding': '5px 10px',
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


def get_terminal_incidence_and_stab(p, which_inc):
    df = get_eqm_vals(p)

    if which_inc=="host":
        S_list = list(df.S)
        I_list = list(df.I)
        term_inc = [I_list[ii]/(S_list[ii] + I_list[ii])
                        for ii in range(len(S_list))]
    else:
        X_list = list(df.X)
        Z_list = list(df.Z)
        term_inc = [Z_list[ii]/(X_list[ii] + Z_list[ii])
                        for ii in range(len(Z_list))]

    stability = list(df.is_stable)

    return term_inc, stability


