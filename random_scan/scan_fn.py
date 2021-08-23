import pandas as pd
import numpy as np
from tqdm import tqdm

from random_scan.pars import RandomParams, RandomParamsDeltaBeta
from model.eqm_fns import RootAnalyser
from utils.fns_model import R0Finder


def run_random_scan(trans_type, n_runs, allow_break=False, delta_beta_case=False):
    
    print(f"Running scan. delta_beta_case={delta_beta_case}")

    br = -1*np.ones(n_runs)
    sb = -1*np.ones(n_runs)
    
    R0_list = -1*np.ones(n_runs)
    kappa_list = -1*np.ones(n_runs)
    max_tol_list = -1*np.ones(n_runs)
    
    all_params = [{}]*n_runs
    coef_list =  [[]]*n_runs

    invalid_total = 0


    for ii in tqdm(range(n_runs)):
        is_valid = False
        invalid_total -= 1

        while not is_valid:
            
            invalid_total += 1

            if delta_beta_case:
                rp = RandomParamsDeltaBeta(trans_type)
            else:
                rp = RandomParams(trans_type)

            RA = RootAnalyser(rp)
            df = RA.df
            
            is_valid = all(df.tol<0.1)

            R0F = R0Finder(rp)

            R0 = R0F.value
            kappa = R0F.kappa

            
            R0_list[ii] = R0
            kappa_list[ii] = kappa
            
            max_tol_list[ii] = max(df.tol)
            br[ii] = sum(df.bio_realistic)
            sb[ii] = sum(df[df.bio_realistic].is_stable)

            coef_list[ii] = {"coef_" + str(ind): item for ind, item in enumerate(RA.coef)}
            all_params[ii] = vars(rp)


        if allow_break and sum(df.bio_realistic)==4:
            break
    


    data = dict(bio_realistic=br,
                stable_BR=sb,
                max_tol=max_tol_list,
                R0s=R0_list,
                kappa=kappa_list)
    
    roots_df = pd.DataFrame(data)
    par_df = pd.DataFrame(all_params)
    coef_df = pd.DataFrame(coef_list)

    out = pd.concat([roots_df, par_df, coef_df], axis=1)

    out['invalid_total'] = invalid_total

    return out

