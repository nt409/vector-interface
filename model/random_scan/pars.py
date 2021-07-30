import numpy as np
import pandas as pd

from .bounds import BOUNDS

unif = np.random.uniform

class RandomParams:
    def __init__(self, trans_type) -> None:
        self.df = pd.DataFrame(BOUNDS)

        self.trans_type = trans_type

        self.is_valid = False
        
        while not self.is_valid:
            self.set_vars()
            self.is_valid = self.check_validity()
        
        delattr(self, "df")
        delattr(self, "is_valid")



    def set_vars(self):
        self.set_random_vars()

        if self.trans_type=="NPT":
            self.set_NPT_vars()
        elif self.trans_type=="PT":
            self.set_PT_vars()
        else:
            raise Exception(f"Invalid trans_type: {self.trans_type}")
        
        self.del_vars()


    def check_validity(self):
        if self.eta<0:
            return False
        return True



    def set_random_vars(self):

        for var in self.df["var"]:
            x = unif(
                self.get_min(var),
                self.get_max(var),
                size=1)[0]
            
            setattr(self, var, x)

    
    def set_NPT_vars(self):
        self.nu_p = self.nu_m
        self.om_p = self.om_m
        self.eps_p = self.eps_m
        self.tau = vars(self)["tau-NPT"]
        self.zeta = vars(self)["zeta-NPT"]
        self.gamma = 1
        self.eta = 1 - self.eps_m * self.om_m
    
        
    def set_PT_vars(self):
        self.tau = vars(self)["tau-PT"]
        self.zeta = vars(self)["zeta-PT"]
        self.gamma = self.om_p
        self.eta = self.eps_m * self.om_m


    def del_vars(self):
        delattr(self, "tau-NPT")
        delattr(self, "tau-PT")
        delattr(self, "zeta-NPT")
        delattr(self, "zeta-PT")


    def get_min(self, var):
        row = self.df[self.df["var"]==var]
        return float(row["min"])
    
    def get_max(self, var):
        row = self.df[self.df["var"]==var]
        return float(row["max"])