import pandas as pd


def obtain_frequency(trans_type, n_runs, seed):
    file_name = f"../csvs/df_{trans_type}_n={n_runs}_s={seed}.csv"
    df = pd.read_csv(file_name)

    freqs = []
    incidence = []

    for ii in range(5):
        fltrd = df[df.bio_realistic==ii]
        nn = fltrd.shape[0]
        
        incidence.append(nn)
        freqs.append(100*nn/n_runs)

    out = pd.DataFrame(dict(n_roots=list(range(5)), incidence=incidence, frequency=freqs))
    out.to_csv(f"../csvs/freq_df_{trans_type}_n={n_runs}_s={seed}.csv")
    # return out

    


if __name__=="__main__":
    n_runs = 1000000
    seed = 3

    obtain_frequency("NPT", n_runs, seed)
    obtain_frequency("PT", n_runs, seed)