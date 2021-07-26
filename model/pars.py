class DefaultParams:
    def __init__(self, trans_type) -> None:

        self.N = 1000

        self.rho = 0.01
        self.mu = 0.01

        self.alpha = 0.12
        self.sigma = 0.18

        self.Gamma = 2

        self.delta = 0
        self.beta = 1
        
        self.nu_m = 1
        self.nu_p = 1

        self.om_m = 0.5
        self.om_p = 0.5
        
        self.eps_m = 1
        self.eps_p = 1

        self.trans_type = trans_type
        
        if trans_type=='NPT':
            self.gamma = 1
            self.eta = 1 - self.eps_m * self.om_m
            self.tau = 4
            self.zeta = 1977.6

        elif trans_type=='PT':
            self.gamma = self.om_p
            self.eta = self.eps_m * self.om_m
            self.tau = 0.05
            self.zeta = 163.2

        else:
            raise Exception("invalid type of transmission specified")

        self.vc = ValidityChecker(self)








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

        self.trans_type = trans_type
        
        if trans_type=='NPT':
            self.gamma = 1
            self.eta = 1 - self.eps_m * self.om_m
        else:
            self.gamma = self.om_p
            self.eta = self.eps_m * self.om_m

        self.vc = ValidityChecker(self)








class ValidityChecker:
    def __init__(self, params) -> None:
        self.params = params
        self.check_validity()
    
    def check_validity(self):
        p = self.params

        self.is_valid = True
        self.error_message = "NA"
        
        if p.tau == 0 and p.alpha == 0:
            self.is_valid = False
            self.error_message = u"Cannot have \u03B1 and \u03C4 both equal to 0"
            return None
        
        if p.om_m * p.eps_m >= 1:
            self.is_valid = False
            self.error_message = u"Cannot have \u03C9\u208B\u03B5\u208B \u2265 1"
            return None

        if p.om_p * p.eps_p >= 1:
            self.is_valid = False
            self.error_message = u"Cannot have \u03C9\u208A\u03B5\u208A \u2265 1"
            return None




