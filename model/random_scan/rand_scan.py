import numpy as np
import pandas as pd
import os

from .fns import run_random_scan
from .plot import plot_quartics



def main(trans_type, n_runs, seed, roots):
    df = check_for_roots(trans_type, n_runs, seed)
    plot_and_save_by_n_roots(df, roots, trans_type, n_runs, seed)




def check_for_roots(trans_type, n_runs, seed):
    np.random.seed(seed)

    file_name = f"../csvs/df_{trans_type}_n={n_runs}_s={seed}.csv"

    if os.path.isfile(file_name):
        print("loading")
        df = pd.read_csv(file_name)

    else:
        print("running")
        df = run_random_scan(trans_type, n_runs)
        df.to_csv(file_name)

    
    print("\n", "number of biologically realistic roots is in", df.bio_realistic.unique(), "\n")

    return df




def plot_and_save_by_n_roots(df, roots, trans_type, n_runs, seed):
    
    for n in roots:
        fltrd = df[df.bio_realistic==n]

        flt_fl_nm = f"../csvs/by_n_roots/tt={trans_type}_nroots={n}_nruns={n_runs}_s={seed}.csv"
        fltrd.to_csv(flt_fl_nm)

        plot_quartics(fltrd, 1)
     


def get_4_eq(trans_type, n_runs, seed):
    np.random.seed(seed)
    df = run_random_scan(trans_type, n_runs, allow_break=True)
    df = df[df.bio_realistic==4]
    file_name = f"../csvs/filt_4_df_{trans_type}_n={n_runs}_s={seed}.csv"
    df.to_csv(file_name)
    


if __name__=="__main__":
    
    run_full_scan = False
    seed = 5

    if run_full_scan:

        # 1M
        n_runs = 1000000
        
        # n_runs = 100

        roots = list(range(5))

        main("NPT", n_runs, seed, roots)
        main("PT", n_runs, seed, roots)
    
    else:
        seed = 4
        # 100M
        n_runs_4 = 100000000
        get_4_eq("NPT", n_runs_4, seed)