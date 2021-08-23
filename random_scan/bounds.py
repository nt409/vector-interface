"""Bounds for variables used in the random scan."""

BOUNDS = [
            # host
            dict(min=1, max=2000, var='N'),
            dict(min=0.001, max=0.05, var='rho'),
            dict(min=0.001, max=0.2, var='mu'),
            
            # vector
            dict(min=0, max=0.6, var='alpha'),
            dict(min=0.001, max=0.4, var='sigma'),
            dict(min=0.001, max=4, var='Gamma'),
            dict(min=0, max=1, var='delta'),
            dict(min=0, max=3, var='beta'),
            
            # defaults for NPT, PT are different
            dict(min=0, max=8, var='tau-NPT'),
            dict(min=0, max=1, var='tau-PT'),
            #
            dict(min=1000, max=2400, var='zeta-NPT'),
            dict(min=1, max=300, var='zeta-PT'),

            # pref
            dict(min=0.001, max=4, var='nu_m'),
            dict(min=0.001, max=4, var='nu_p'),
            dict(min=0.001, max=1, var='om_m'),
            dict(min=0.001, max=1, var='om_p'),
            dict(min=0.001, max=2, var='eps_m'),
            dict(min=0.001, max=2, var='eps_p'),
            ]            