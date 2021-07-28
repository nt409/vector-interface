from components.helper_fns import slider_list

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

        correct_number = 19
        
        if len(pars)!=correct_number:
            raise Exception(f"Wrong number of parameters specified: {len(pars)}, should be {correct_number}. {pars}")

        self.trans_type = trans_type

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

        
        if trans_type=='NPT':
            nu = pars[16]
            omega = pars[17]
            epsilon = pars[18]
            # preference pars - same for NPT
            self.nu_m = nu
            self.nu_p = nu

            self.om_m = omega
            self.om_p = omega
            
            self.eps_m = epsilon
            self.eps_p = epsilon

            # gamma and eta different form for PT vs NPT
            self.gamma = 1
            self.eta = 1 - self.eps_m * self.om_m

        else:
            # preference pars - differ for PT
            self.nu_m = pars[10]
            self.nu_p = pars[11]

            self.om_m = pars[12]
            self.om_p = pars[13]
            
            self.eps_m = pars[14]
            self.eps_p = pars[15]

            # gamma and eta different form for PT vs NPT
            self.gamma = self.om_p
            self.eta = self.eps_m * self.om_m

        self.vc = ValidityChecker(self)








class ValidityChecker:
    def __init__(self, Param) -> None:
        self.Param = Param

        self.check_validity()
    
    def check_validity(self):
        p = self.Param

        self.is_valid = True
        self.error_message = "NA"
        
        if p.tau==0 and p.alpha==0:
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

        self.check_variables_within_bds()

        if p.trans_type=="NPT":
            self.check_pref_vars_equal()
        



    def check_variables_within_bds(self):
        for sld_dict in slider_list[:-4]:
            key = sld_dict['var']
            
            if key in ["nu", "om", "eps"]:
                if self.Param.trans_type=="NPT":
                    self.check_this_var_in_bds(sld_dict, f"{key}_p")
                    self.check_this_var_in_bds(sld_dict, f"{key}_m")

            else:
                self.check_this_var_in_bds(sld_dict, key)
                    

    def check_this_var_in_bds(self, sld_dict, var_name):
        x = getattr(self.Param, var_name)

        var_min = sld_dict['min']
        var_max = sld_dict['max']
        
        if x<var_min or x>var_max:
            raise Exception(f"{var_name} is out of its valid range: [{var_min},{var_max}]")


    def check_pref_vars_equal(self):
        for var in ["om", "nu", "eps"]:
            x_m = getattr(self.Param, f"{var}_m")
            x_p = getattr(self.Param, f"{var}_p")

            if x_m!=x_p:
                raise Exception(f"{var}_m should equal {var}_p, but they have values {x_m}, {x_p}")


