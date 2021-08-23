import pandas as pd

from .config import config_use
from model.eqm_fns import RootAnalyser



def main(config):
    df = get_df(config)
    test_df_rows(df)




def get_df(config):
    n_runs = config["n_runs"]
    seed = config["seed"]
    delta_beta_case = config["delta_beta_case"]

    file_str = f"n={n_runs}_s={seed}"

    if delta_beta_case:
        db_str = "delta_beta"
    else:
        db_str = ""

    file_name_bad = f"../csvs/bad_tol/{file_str}_{db_str}.csv"

    df = pd.read_csv(file_name_bad, float_precision='round_trip')

    return df


def test_df_rows(df):
    for ii in range(min(10,df.shape[0])):
        row = df.iloc[ii,:]

        print(row.max_tol)

        RA = RootAnalyser(row)
        eqbria = RA.df
        
        print(RA.coef)
        print([rr for rr in row[-7:-2]])
        print(eqbria.tol)



if __name__=="__main__":
    main(config_use)