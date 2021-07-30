import numpy as np
import pandas as pd
import os

from .fns import run_random_scan
from .plot import plot_quartics




def check_for_roots_and_plot(trans_type, n_runs, seed):
    np.random.seed(seed)

    file_name = f"../df_{trans_type}_n={n_runs}_s={seed}.csv"

    if os.path.isfile(file_name):
        print("loading")
        df = pd.read_csv(file_name)

    else:
        print("running")
        df = run_random_scan(trans_type, n_runs)
        df.to_csv(file_name)

    
    print("\n", "number of biologically realistic roots is in", df.bio_realistic.unique(), "\n")

    for n in range(5):
        fltrd = df[df.bio_realistic==n]
        print(fltrd)
        plot_quartics(fltrd, 1)
    

    


if __name__=="__main__":
    seed = 3

    n_runs = 100000
    # n_runs = 10

    check_for_roots_and_plot("NPT", n_runs, seed)
    check_for_roots_and_plot("PT", n_runs, seed)
