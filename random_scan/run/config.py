"""Different configurations for parameter scan."""

# 1M
conf_normal = dict(
    seed = 6,
    n_runs = 1000000,
    delta_beta_case=False,
    )


# 1M
conf_delta_beta = dict(
    seed = 6,
    n_runs = 1000000,
    delta_beta_case=True,
    )



conf_small = dict(
    seed = 6,
    n_runs = 10,
    delta_beta_case=False
    )

# 1M
conf_4_eq = dict(
    # n_runs = 1000000,
    n_runs = 10,
    delta_beta_case=False
    )


config_use = conf_normal
# config_use = conf_delta_beta