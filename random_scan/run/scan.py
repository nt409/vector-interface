"""Run scan across different parameters in NPT and PT cases"""

import numpy as np
import pandas as pd
import os

from random_scan.scan_fn import run_random_scan
# from random_scan.plot import plot_by_n_roots

from .config import config_use



def main(trans_type, n_runs, seed, roots, delta_beta_case):
    db_str = "delta_beta" if delta_beta_case else ""
    file_str = f"{db_str}_n={n_runs}_s={seed}_{trans_type}.csv"
    
    df = get_random_scan_df(trans_type, n_runs, seed, delta_beta_case, file_str)

    save_by_n_roots(df, roots, file_str)

    # plot_by_n_roots(df, roots)






def get_random_scan_df(trans_type, n_runs, seed, db_case, file_str):
    np.random.seed(seed)

    file_name = f"../csvs/main/{file_str}"

    # if False:
    if os.path.isfile(file_name):
        print("loading")
        df = pd.read_csv(file_name, float_precision='round_trip')

    else:
        print("running")
        df = run_random_scan(trans_type, n_runs, allow_break=False,
                                        delta_beta_case=db_case)
        
        df.to_csv(file_name, index=False)
    
    print("\n", "number of biologically realistic roots is in", df.bio_realistic.unique(), "\n")

    return df




def save_by_n_roots(df, roots, file_str):
    for n in roots:
        fltrd = df[df.bio_realistic==n]
        file_name = f"../csvs/by_n_roots/{file_str}"
        fltrd.to_csv(file_name, index=False)


    





if __name__=="__main__":
    
    n_runs = config_use['n_runs']
    seed = config_use['seed']
    db_case = config_use['delta_beta_case']

    roots = list(range(5))

    main("NPT", n_runs, seed, roots, db_case)
    main("PT", n_runs, seed, roots, db_case)

