"""Get frequency df for table in paper."""

import pandas as pd
from .config import config_use




def get_freq_df(n_runs, seed, delta_beta_case):
    
    file_str = f"n={n_runs}_s={seed}"

    if delta_beta_case:
        db_str = "delta_beta"
    else:
        db_str = ""

    file_str_db = file_str + "_" + db_str

    file_name_NPT = f"../csvs/main/{db_str}_{file_str}_NPT.csv"
    file_name_PT = f"../csvs/main/{db_str}_{file_str}_PT.csv"

    file_name_comb = f"../csvs/combined/{file_str_db}.csv"
    file_name_bad = f"../csvs/bad_tol/{file_str_db}.csv"


    df_NPT = pd.read_csv(file_name_NPT, float_precision='round_trip')
    df_NPT['trans_type'] = "NPT"

    df_PT = pd.read_csv(file_name_PT, float_precision='round_trip')
    df_PT['trans_type'] = "PT"
    


    df = pd.concat([df_NPT, df_PT], axis="rows")

    df["kappa_pos"] = df.loc[:, "kappa"]>0

    df["R0_above_1"] = df.loc[:, "R0s"]>1



    df.to_csv(file_name_comb, index=False)


    bad_df = df.loc[df.max_tol>0.1]
    bad_df.to_csv(file_name_bad, index=False)

    
    
    
    good_df = df.loc[df.max_tol<0.1]

    levels_list = [
                ["kappa_pos", "R0_above_1", "bio_realistic", "stable_BR"],

                # ["kappa_pos", "R0_above_1", "bio_realistic"],
                # ["kappa_pos", "R0_above_1", "stable_BR"],
                # ["R0_above_1", "bio_realistic", "stable_BR"],

                # ["bio_realistic", "stable_BR"],
                # ["kappa_pos", "R0_above_1"],
                # ["R0_above_1", "bio_realistic"],
                # ["R0_above_1", "stable_BR"],

                # ["R0_above_1"],
                # ["bio_realistic"],
                # ["stable_BR"],
                ]

    for levels in levels_list:
        get_df_and_save(good_df, levels, file_str_db)
    










def get_df_and_save(df, levels, file_str_db):
    levels_use = ["trans_type"] + levels

    grouped = df.groupby(levels_use)

    gg = grouped.kappa.agg([len])
    out = gg.reset_index()
    out = out.rename(columns={'len': 'n'})

    n_NPT = out.loc[out['trans_type']=='NPT'].n.sum()
    n_PT = out.loc[out['trans_type']=='PT'].n.sum()

    n_NPT_val = out.loc[(out['trans_type']=='NPT') &
                        (out['bio_realistic']>0)].n.sum()
    
    n_PT_val = out.loc[(out['trans_type']=='PT') &
                        (out['bio_realistic']>0)].n.sum()

    out["inc, (% by trans. type)"] = out.apply(lambda row: get_simple_percent(row, n_NPT, n_PT),
                                                    axis='columns')
    
    out["inc, (% by trans. type of >0 eqa)"] = out.apply(lambda row: 
                                get_percent_if_valid(row, n_NPT_val, n_PT_val),
                                                axis='columns')

    if len(levels)==4:
        var_str = "ALL"
    else:
        var_str = ",".join([e[:3] for e in levels])

    out.to_csv(f"../csvs/for_paper/{var_str}_{file_str_db}.csv", index=False)



def get_simple_percent(row, n_NPT, n_PT):
    return (100* row.n / n_NPT if row.trans_type=="NPT" 
                                                else 100* row.n / n_PT)

def get_percent_if_valid(row, n_NPT, n_PT):
    if row.bio_realistic==0:
        return "NA"

    return (100* row.n / n_NPT if row.trans_type=="NPT" 
                                                else 100* row.n / n_PT)






if __name__=="__main__":
    
    n_runs = config_use['n_runs']
    seed = config_use['seed']
    db_case = config_use['delta_beta_case']

    print(f"\n Finding output freq dataframes for paper Table.\n Case: {'delta=0, beta=1 case' if db_case else 'general'}")

    get_freq_df(n_runs, seed, db_case)