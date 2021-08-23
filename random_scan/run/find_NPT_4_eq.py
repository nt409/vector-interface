"""Seek example with 4 equilibria in the NPT case."""

import numpy as np
import sys

from random_scan.scan_fn import run_random_scan
from random_scan.run.config import conf_4_eq


def get_4_eq(trans_type, n_runs, seed):
    np.random.seed(seed)
    
    df = run_random_scan(trans_type, n_runs, allow_break=True, delta_beta_case=False)
    df = df[df.bio_realistic==4]
    
    if not df.shape[0]:
        df.loc[0, 'result'] = "Did not find any runs with 4 equilibria"
        name_out = "found_none"
    else:
        df.loc[0, 'result'] = "Found some runs with 4 equilibria!"
        name_out = "found_some"

    file_name = f"../csvs/eq_4/df_{trans_type}_n={n_runs}_s={seed}_{name_out}.csv"
    df.to_csv(file_name, index=False)
    




if __name__=="__main__":
    
    conf = conf_4_eq
    
    n_runs = conf['n_runs']

    if len(sys.argv)==2:
        seed = int(sys.argv[1])
        get_4_eq("NPT", n_runs, seed)
    else:
        raise Exception("Supply a random seed argument")
