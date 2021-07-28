import dash_table
import pandas as pd


from utils.figures import ModelRunFigure
from utils.fns_general import get_kappa

from model.eqm_fns import RootAnalyser, StabilityMatrix
from model.simulator import Simulator



def get_soln(p, itl_cnds):
        
    sim = Simulator(p, itl_cnds)
    sim.run()

    return sim.out




def get_init_cnds(p, default_or_custom, N, *init_cond_pars):
    kappa = get_kappa(p)
    
    if default_or_custom=="def-NPT":
        return [999, 1, kappa-1, 1]
    elif default_or_custom=="def-PT":
        return [999, 1, kappa-1, 1]
    elif default_or_custom=="def-C":
        check_kappa_positive(kappa)
        out = get_custom_init_conds(kappa, N, *init_cond_pars)
        return out
    else:
        raise Exception("invalid transmission type entered")


def check_kappa_positive(kappa):
    if kappa<0:
        raise Exception("Kappa negative. Not strictly an error but causes " +
                "problems... R0 imaginary, vectpr incidence tending to infinity" + 
                "initial conditions in this form would be neg")
    


def get_custom_init_conds(kappa, N, *init_cond_pars):

    host_inc = init_cond_pars[0]
    host_prop = init_cond_pars[1]
    vec_inc = init_cond_pars[2]
    vec_prop = init_cond_pars[3]

    S0 = N * host_prop * (1-host_inc)
    I0 = N * host_prop * host_inc
    
    X0 = kappa * vec_prop * (1-vec_inc)
    Z0 = kappa * vec_prop * vec_inc

    return [S0, I0, X0, Z0]



def get_host_fig(soln):

    xs = [soln.t, soln.t]
    ys = [soln.S, soln.I]
    clrs = ["#00b050", "#c00000"]
    names = ["Susceptible: S", "Infected: I"]

    data = dict(xs=xs, ys=ys, clrs=clrs, names=names)

    fig = ModelRunFigure(data, "Number of hosts").fig
    
    return fig



def get_vec_fig(soln):
    
    xs = [soln.t, soln.t]
    ys = [soln.X, soln.Z]
    clrs = ["#92d050", "#e46c0a"]
    names = ["Nonviruliferous: X", "Viruliferous: Z"]

    data = dict(xs=xs, ys=ys, clrs=clrs, names=names)
    
    fig = ModelRunFigure(data, "Number of vectors").fig
    
    return fig


def get_inc_fig(soln):
    
    xs = [soln.t, soln.t]
    
    y1 = [(soln.I[ii])/(soln.I[ii] + soln.S[ii]) for ii in range(len(soln.S))]
    
    y2 = [(soln.Z[ii])/(soln.Z[ii] + soln.X[ii]) if
                     (soln.Z[ii]>0 and soln.X[ii]>0) else 
                            None for ii in range(len(soln.X))]
    
    ys = [y1, y2]

    clrs = ["rgb(255,202,211)", "rgb(151,11,238)"]

    names = ["Host incidence: I/(S+I)", "Vector incidence: Z/(X+Z)"]

    data = dict(xs=xs, ys=ys, clrs=clrs, names=names)

    fig = ModelRunFigure(data, "Incidence").fig
    
    return fig




class EqmTable:
    def __init__(self, p) -> None:
        self.params = p
        self.tab = self.get_table()

    def get_table(self):
        p = self.params

        rta = RootAnalyser(p)
        
        df = rta.df

        df = df[df['bio_realistic']]

        df = df.drop(columns=["solves_system", "tol", "bio_realistic"])

        dis_f_eqm = self.get_dis_free_eqm_dict()

        if dis_f_eqm is not None:    
            df = df.append(dis_f_eqm, ignore_index=True)
        
        dis_f_eqm_nv = self.get_dis_free_eqm_dict_no_vec()
        
        df = df.append(dis_f_eqm_nv, ignore_index=True)

        df = df.round(3)

        for ind in ["S", "I", "X", "Z", "host_inc", "vec_inc"]:
            df[ind] = df[ind].astype(float)

        df["is_stable"] = [str(ee).capitalize() for ee in df["is_stable"]]

        df.columns = list(df.columns[:-3]) + ["Host incidence", "Vector incidence", "Stable?"]

        return my_table(df)



    def get_dis_free_eqm_dict(self):
        p = self.params

        kappa = get_kappa(p)

        if kappa<0:
            return None
        
        dis_free_eqm = [p.N, 0, kappa, 0]
        
        stab = StabilityMatrix(p, dis_free_eqm).is_stable

        return dict(S=p.N,
                I=0,
                X=kappa,
                Z=0,
                host_inc=0,
                vec_inc=0,
                is_stable=stab,
                )


    def get_dis_free_eqm_dict_no_vec(self):
        p = self.params

        dis_free_eqm_no_vec = [p.N, 0, 0, 0]
        
        stab = StabilityMatrix(p, dis_free_eqm_no_vec).is_stable

        return dict(S=p.N,
                I=0,
                X=0,
                Z=0,
                host_inc=0,
                vec_inc=0,
                is_stable=stab,
                )



def get_R0_kappa_table(p):

    kappa = get_kappa(p)

    R0_val = R0Finder(p).value

    data = dict(R0=[R0_val], kappa=[kappa])
    
    df = pd.DataFrame(data)

    df = df.round(3)

    df.columns = [u"R\u2080", u"\u03BA"]

    return my_table(df)





class R0Finder:
    def __init__(self, params) -> None:
        self.params = params
        self.kappa = get_kappa(params)

        self.value = self.get_R0()

    def get_R0(self):
        
        R_PV = self.get_RPV()
        R_VP = self.get_RVP()

        out = (R_PV * R_VP)**(0.5)
        return out

    def get_RPV(self):
        p = self.params
        kappa = self.kappa

        num = kappa * p.eta * p.nu_m
        denom = p.N * p.om_m * p.Gamma * (p.mu + p.rho)
        out = num/denom
        return out

    def get_RVP(self):
        p = self.params

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
