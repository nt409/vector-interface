import numpy as np
from scipy.integrate import ode

from model.eqm_fns import ODESystem



class Simulator:
    def __init__(self, params, initial_conds) -> None:
        self.params = params

        self.out = ModelOutput()

        self.ode_sys = ODESystem(params)

        self.setup_solver(initial_conds)


    def run(self):
        self.update_system(0)
        for ind, tt in enumerate(self.out.t[1:]):
            if not self.solver.successful():
                raise RuntimeError('ode solver unsuccessful')
            else:
                self.solver.integrate(tt)
                self.update_system(ind+1)

        


    def setup_solver(self, initial_conds):
        odeSolver = ode(self.ode_sys.system)
        odeSolver.set_integrator('dopri5', max_step=10)
        odeSolver.set_initial_value(initial_conds, self.out.t[0])
        self.solver = odeSolver


    def update_system(self, ind):
        self.out.S[ind] = self.solver.y[0]
        self.out.I[ind] = self.solver.y[1]
        self.out.X[ind] = self.solver.y[2]
        self.out.Z[ind] = self.solver.y[3]




class ModelOutput:
    def __init__(self) -> None:
        n_points = 400

        self.S = np.zeros(n_points)
        self.I = np.zeros(n_points)
        self.X = np.zeros(n_points)
        self.Z = np.zeros(n_points)

        self.t = self.get_t(n_points)
    
    @staticmethod
    def get_t(n_points):
        # Not using linspace bc fast initial transient dynamics

        n1 = 200
        n2 = n_points + 1 - n1
        divider = 40

        t1 = np.linspace(0, divider, n1)
        t2 = np.linspace(divider, 600, n2)

        return np.concatenate([t1[:-1],t2])
