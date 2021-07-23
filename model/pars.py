class DefaultParams:
    def __init__(self, trans_type) -> None:

        self.N = 1000

        self.rho = 0.01
        self.mu = 0.01

        self.alpha = 0.12
        self.tau = 4
        self.sigma = 0.18        
        self.zeta = 1977.6

        self.Gamma = 2

        self.delta = 0
        self.beta = 1
        
        self.nu_m = 1
        self.nu_p = 1

        self.om_m = 0.5
        self.om_p = 0.5
        
        self.eps_m = 1
        self.eps_p = 1
        
        if trans_type=='NPT':
            self.gamma = 1
            self.eta = 1 - self.eps_m * self.om_m
        elif trans_type=='PT':
            self.gamma = self.om_p
            self.eta = self.eps_m * self.om_m
        else:
            raise Exception("invalid type of transmission specified")







class CustomParams:
    def __init__(self, trans_type, *pars) -> None:

        self.N = pars[0]

        self.rho = pars[1]
        self.mu = pars[2]

        self.alpha = pars[3]
        self.tau = pars[4]
        self.sigma = pars[5]        
        self.zeta = pars[6]

        self.Gamma = pars[7]

        self.delta = pars[8]
        self.beta = pars[9]
        
        self.nu_m = pars[10]
        self.nu_p = pars[11]

        self.om_m = pars[12]
        self.om_p = pars[13]
        
        self.eps_m = pars[14]
        self.eps_p = pars[15]
        
        if trans_type=='NPT':
            self.gamma = 1
            self.eta = 1 - self.eps_m * self.om_m
        else:
            self.gamma = self.om_p
            self.eta = self.eps_m * self.om_m








