import pandas as pd
import numpy as np

from model.eqm_fns import RootAnalyser
from model.simulator import Simulator
from utils.fns_model import get_host_fig, get_vec_fig


def get_first_row(trans_type, n_roots, n_runs, seed):
    filename = f"../by_n_roots/tt={trans_type}_nroots={n_roots}_nruns={n_runs}_s={seed}.csv"
    df = pd.read_csv(filename)
    
    if df.shape[0]:
        return df.iloc[0, :]

        # for ii in range(df.shape[0]):
        #     row = df.iloc[ii, :]

        #     eq = RootAnalyser(row).df
        #     if sum(eq.is_stable)<2:
        #         return row

        # raise Exception("no rows with no stability")
    else:
        raise Exception(f"Cannot get first row; df has shape: {df.shape}")



def get_ICs(eqbria, which_eq, pertubation):
    S0 = eqbria.iloc[which_eq,0] + pertubation[0]
    I0 = eqbria.iloc[which_eq,1] + pertubation[1]
    X0 = eqbria.iloc[which_eq,2] + pertubation[2]
    Z0 = eqbria.iloc[which_eq,3] + pertubation[3]

    return [S0, I0, X0, Z0]

    
def get_figs(row, ICs):
    sim = Simulator(row, ICs)

    sim.out.t = np.linspace(0,800,400)
    sim.run()
    soln = sim.out

    fig = get_host_fig(soln)
    fig.update_layout(height=400, width=600)
    fig.write_image(f"../{row.trans_type}_host_eq_plot_{row.bio_realistic}.png")
    fig.show()

    fig = get_vec_fig(soln)
    fig.update_layout(height=400, width=600)
    fig.write_image(f"../{row.trans_type}_vec_eq_plot_{row.bio_realistic}.png")
    fig.show()




if __name__=="__main__":
    n_runs = 1000000
    seed = 3
    roots = 4

    row = get_first_row("PT", roots, n_runs, seed)

    eqbria = RootAnalyser(row).df

    print("\n Equilibria:")
    print(eqbria)

    # for which_eq in range(4):
    # pertubation = [1,-1,-0.1,0]
    which_eq = 2
    pertubation = [0,0.1,0,0]

    ICs = get_ICs(eqbria, which_eq, pertubation)

    get_figs(row, ICs)
        


