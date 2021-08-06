import pandas as pd
from tqdm import tqdm

from .pars import RandomParams
from model.eqm_fns import RootAnalyser


def run_random_scan(trans_type, n_runs, allow_break=False):
    br = []
    sb = []
    all_params = []
    coef_list = []

    for _ in tqdm(range(n_runs)):

        rp = RandomParams(trans_type)
        RA = RootAnalyser(rp)
        df = RA.df

        coef_list.append(RA.coef)

        all_params.append(vars(rp))

        n_BR = sum(df.bio_realistic)
        n_SB = sum(df[df.bio_realistic].is_stable)

        br.append(n_BR)
        sb.append(n_SB)

        if allow_break and n_BR==4:
            break



    data = dict(bio_realistic=br, stable_BR=sb, coefficients=coef_list)
    
    roots_df = pd.DataFrame(data)
    par_df = pd.DataFrame(all_params)


    out = pd.concat([roots_df, par_df], axis=1)

    return out

