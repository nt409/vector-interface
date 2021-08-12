import pandas as pd
from tqdm import tqdm

from .pars import RandomParams
from model.eqm_fns import RootAnalyser
from utils.fns_model import R0Finder


def run_random_scan(trans_type, n_runs, allow_break=False):
    br = []
    sb = []
    all_params = []
    coef_list = []
    R0_list = []
    kappa_list = []

    for _ in tqdm(range(n_runs)):

        rp = RandomParams(trans_type)
        RA = RootAnalyser(rp)
        df = RA.df

        R0F = R0Finder(rp)

        R0 = R0F.value
        kappa = R0F.kappa

        coef_list.append(RA.coef)

        all_params.append(vars(rp))

        n_BR = sum(df.bio_realistic)
        n_SB = sum(df[df.bio_realistic].is_stable)

        br.append(n_BR)
        sb.append(n_SB)

        R0_list.append(R0)
        kappa_list.append(kappa)


        if allow_break and n_BR==4:
            break
    

    data = dict(bio_realistic=br, stable_BR=sb, coefficients=coef_list, R0s=R0_list, kappa=kappa_list)
    
    roots_df = pd.DataFrame(data)
    par_df = pd.DataFrame(all_params)

    out = pd.concat([roots_df, par_df], axis=1)

    return out

