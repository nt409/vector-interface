"""
Get figures for paper from different scans. 

Can pick
"""

import pandas as pd
import numpy as np

from model.eqm_fns import RootAnalyser
from model.simulator import Simulator
from utils.fns_model import get_host_fig, get_vec_fig
from random_scan.run.config import config_use





def get_grouped_df(n_runs, seed):
    filename = f"../csvs/combined/n={n_runs}_s={seed}_.csv"

    df = pd.read_csv(filename, float_precision='round_trip')

    grouped = df.groupby(["trans_type", "kappa_pos", "R0_above_1", "bio_realistic", "stable_BR"])
    out = grouped.first().reset_index()

    out = out.loc[out['stable_BR']==2]
    
    # out = out[out["kappa_pos"]]
    # out = out.drop("kappa_pos")

    fn = f"../csvs/to_plot/n={n_runs}_s={seed}_.csv"
    out.to_csv(fn, index=False)

    return out




def plot_via_loop(df):

    for ii in range(df.shape[0]):
        row = df.iloc[ii,:]

        print("\n")
        print(row)

        eqbria = RootAnalyser(row).df

        print("\n")
        print(eqbria)

        eqbria = eqbria.loc[(eqbria.bio_realistic)]

        plot_this_row(row, eqbria)




def plot_this_row(row, eqbria):

    for eq in range(eqbria.shape[0]):

        file_str = (
            f"{n_runs}_{seed}_{row.trans_type}_{row.kappa_pos}_"
            f"{row.R0_above_1}_{int(row.bio_realistic)}_"
            f"{int(row.stable_BR)}_{eq}"
            )
        
        perturbation = [0,0,0,0]

        ICs = get_ICs(eqbria, eq, perturbation)

        soln = get_soln(row, ICs)

        get_figs(soln, file_str)





def get_ICs(eqbria, eq, perturbation):
    S0 = eqbria.iloc[eq,0] + perturbation[0]
    I0 = eqbria.iloc[eq,1] + perturbation[1]
    X0 = eqbria.iloc[eq,2] + perturbation[2]
    Z0 = eqbria.iloc[eq,3] + perturbation[3]

    return [S0, I0, X0, Z0]




def get_soln(row, ICs):
    sim = Simulator(row, ICs)
    sim.out.t = np.linspace(0,800,400)
    sim.run()
    soln = sim.out
    return soln


    
def get_figs(soln, file_str):

    fig = get_host_fig(soln)
    fig.update_layout(height=400, width=600)
    fig.write_image(f"../figs/{file_str}_host_eq_plot.png")
    # fig.show()

    fig = get_vec_fig(soln)
    fig.update_layout(height=400, width=600)
    fig.write_image(f"../figs/{file_str}_vec_eq_plot.png")
    # fig.show()




if __name__=="__main__":
    
    n_runs = config_use['n_runs']
    seed = config_use['seed']

    df = get_grouped_df(n_runs, seed)

    print(df.head(20))
    exit()

    print("\n", df)

    plot_via_loop(df)
    


