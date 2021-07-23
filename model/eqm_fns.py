import pandas as pd
import numpy as np


class ODESystem:
    def __init__(self, params) -> None:
        self.params = params

    def system(self, t, y_vec):
        p = self.params

        S = y_vec[0]
        I = y_vec[1]
        X = y_vec[2]
        Z = y_vec[3]

        out = [
            # dS
            p.rho * (p.N - S) - self.Lambda(S, I, Z),
            # dI
            self.Lambda(S, I, Z) - (p.rho + p.mu) * I,
            # dX
            self.g(S, I, X, Z) + p.tau * Z
                 - self.Omega(S, I, X) - self.h_m(S,I) * X,
            # dZ
            self.Omega(S, I, X) - p.tau * Z
                 - self.h_p(S,I) * Z,
            ]
        return out

    def Lambda(self, S, I, Z):
        p = self.params

        frac = S/ (S + p.nu_p*I)

        out = self.phi_p(S,I) * p.gamma * Z * frac
        return out
    
    def Omega(self, S, I, X):
        p = self.params

        frac = (p.nu_m*I) / (S + p.nu_m*I)

        out = self.phi_m(S,I) * p.eta * X * frac
        return out
    
    def g(self, S, I, X, Z):
        p = self.params

        ib1 = (p.nu_m * p.eps_m * X) / (S + p.nu_m * p.eps_m * I)
        ib2 = (p.nu_p * p.eps_p * Z) / (S + p.nu_p * p.eps_p * I)

        inner_bracket = ib1 + ib2

        first_bracket = X + Z + (p.beta-1)* I *inner_bracket
        
        final_bracket = 1 - (X + Z)/p.zeta

        out = p.sigma * first_bracket * final_bracket

        return out

    def h_p(self, S, I):
        p = self.params

        out = p.alpha * (1 + p.delta* (p.Gamma*self.phi_p(S,I) - 1))
        return out

    def h_m(self, S, I):
        p = self.params

        out = p.alpha * (1 + p.delta* (p.Gamma*self.phi_m(S,I) - 1))
        return out

    def phi_p(self, S, I):
        p = self.params

        num = S + p.nu_p*I
        denom = p.om_p * p.Gamma * (S + p.nu_p * p.eps_p *I)
        
        out = num/denom

        return out

    def phi_m(self, S, I):
        p = self.params

        num = S + p.nu_m*I
        denom = p.om_m * p.Gamma * (S + p.nu_m * p.eps_m *I)
        
        out = num/denom

        return out















class EqmFinder:
    def __init__(self, params, I) -> None:
        self.params = params
        self.I = I
        self.get_S()
        self.get_X()
        self.get_Z()


    def get_S(self):
        p = self.params

        L = 1 + p.mu/p.rho

        self.S = p.N - L * self.I


    def get_X(self):
        # needs self.S

        p = self.params
        I = self.I
        S = self.S

        consts = (p.rho + p.mu) * p.om_m * p.Gamma

        num = consts * (S + p.nu_m * p.eps_m * I) * self.J(I)
        denom = p.gamma * p.eta *p.nu_m * S
        
        self.X = num/denom


    def get_Z(self):
        # needs self.S

        p = self.params
        I = self.I
        S = self.S

        consts = (p.rho + p.mu) * p.om_p * p.Gamma

        num = consts * (S + p.nu_p * p.eps_p * I) * I
        denom = p.gamma * S
        
        self.Z = num/denom


    def J(self, I):
        p = self.params
        
        I = self.I
        S = self.S
        
        K = p.tau + p.alpha - p.alpha*p.delta

        first = K* p.om_p * p.Gamma * (S + p.nu_p * p.eps_p * I)
        second = p.alpha * p.delta * p.Gamma * (S + p.nu_p * I)

        out = first + second

        return out












class Quartic:
    def __init__(self, params) -> None:
        self.get_coefficients(params)

    def get_coefficients(self, p):

        self.get_consts(p)

        self.J0 = self.get_J0(p)
        self.J1 = self.get_J1(p)

        self.P0 = self.get_P0(p)
        self.P1 = self.get_P1(p)
        self.P2 = self.get_P2(p)

        self.Q0 = self.get_Q0(p)
        self.Q1 = self.get_Q1(p)
        self.Q2 = self.get_Q2(p)

        self.R0 = self.get_R0(p)
        self.R1 = self.get_R1(p)
        self.R2 = self.get_R2(p)
        
        self.a0 = self.get_a0(p)
        self.a1 = self.get_a1(p)
        self.a2 = self.get_a2(p)
        self.a3 = self.get_a3(p)
        self.a4 = self.get_a4(p)

        self.coefficients = [self.a4, self.a3, self.a2, self.a1, self.a0]

    def get_consts(self, p):
        self.L = 1 + p.mu/p.rho
        self.A = (p.tau + p.alpha - p.alpha*p.delta) * p.om_p * p.Gamma
        self.B = p.alpha * p.delta * p.Gamma
        self.C = ((p.mu + p.rho) * p.Gamma) / (p.gamma * p.eta * p.nu_m)


    def get_a0(self, p):
        out = (p.sigma * self.P0 * self.R0 -
                p.alpha * p.zeta * p.N * self.Q0)
        return out
        
    def get_a1(self, p):
        out = (p.sigma * (self.P0 * self.R1
                    + self.P1 * self.R0)
            + p.alpha * p.zeta * (self.Q0 * self.L 
                    - self.Q1 * p.N)
                )
        return out

    def get_a2(self, p):
        out = (p.sigma * (self.P0 * self.R2
                    + self.P1 * self.R1
                    + self.P2 * self.R0)
            + p.alpha * p.zeta * (self.Q1 * self.L 
                    - self.Q2 * p.N)
                )
        return out

    def get_a3(self, p):
        out = (p.sigma * (self.P1 * self.R2
                    + self.P2 * self.R1)
            + p.alpha * p.zeta * self.Q2 * self.L 
                )
        return out
    
    def get_a4(self, p):
        out = p.sigma * self.P2 * self.R2
        return out

    def get_J0(self, p):
        return (self.A + self.B) * p.N

    def get_J1(self, p):
        out = (self.A * p.nu_p * p.eps_p + self.B * p.nu_p
                     - (self.A + self.B) * self.L)
        return out

    def get_P0(self, p):
        out = p.zeta * p.N - self.C * p.om_m * self.J0 * p.N
        return out

    def get_P1(self, p):
        out = (- p.zeta * self.L
                 - self.C * (p.om_m * self.J0 * (p.nu_m * p.eps_m - self.L)
                 + p.om_m * self.J1 * p.N
                 + p.eta * p.nu_m * p.om_p * p.N))
        return out

    def get_P2(self, p):
        out = ( - self.C * (p.om_m * self.J1 * (p.nu_m * p.eps_m - self.L)
                 + p.eta * p.nu_m * p.om_p * (p.nu_p * p.eps_p - self.L)))
        return out

    def get_Q0(self, p):
        out = ((1-p.delta) * p.om_m * p.N * self.J0 
                    + p.delta * p.N * self.J0)
        return out

    def get_Q1(self, p):
        out = ((1-p.delta) * (p.om_m * p.N * self.J1 
                    + p.om_m * (p.nu_m * p.eps_m - self.L)* self.J0
                    + p.eta * p.nu_m * p.om_p * p.N)
                + p.delta * (p.N * self.J1
                    + (p.nu_m - self.L) * self.J0
                    + p.eta * p.nu_m * p.N
                    ))
        return out

    def get_Q2(self, p):
        out = ((1-p.delta) * (
                    p.om_m * (p.nu_m * p.eps_m - self.L) * self.J1
                + p.eta * p.nu_m * p.om_p * (p.nu_p * p.eps_p - self.L) )
            + p.delta * ((p.nu_m - self.L) * self.J1
                + p.eta * p.nu_m * (p.nu_p - self.L)
                ))
        return out
    
    def get_R0(self, p):
        out = p.om_m * p.N * self.J0 
        return out

    def get_R1(self, p):
        out = ((p.om_m * p.N * self.J1 
                    + p.om_m * (p.nu_m * p.eps_m - self.L)* self.J0
                    + p.eta * p.nu_m * p.om_p * p.N)
            + (p.beta - 1) * p.nu_m * p.om_m * p.eps_m * self.J0)
        return out

    def get_R2(self, p):
        out = ((p.om_m * (p.nu_m * p.eps_m - self.L) * self.J1
                + p.eta * p.nu_m * p.om_p * (p.nu_p * p.eps_p - self.L))
            + (p.beta - 1) * (
                p.nu_m * p.eps_m * p.om_m * self.J1 
                + p.eta * p.nu_m * p.nu_p * p.eps_p * p.om_p)
                )
        return out





class RootAnalyser:
    def __init__(self, params) -> None:
        self.params = params

        self.find_roots()

        self.analyse_roots()        


    def find_roots(self):
        p = self.params

        q = Quartic(p)
        coef = q.coefficients
        
        self.roots = np.roots(coef)


    def analyse_roots(self):
        self.check_roots_in_range()
        self.check_solves_system()
        self.find_equilibria()
        self.check_stability()
        self.get_df()


    def check_roots_in_range(self):
        self.roots_in_range = [self.check_in_range(rr) for rr in self.roots]

    def check_in_range(self, n):
        p = self.params

        L = 1 + p.mu/p.rho

        if np.iscomplex(n) or n<0 or n>p.N/L:
            return False
        else:
            return True

    def check_solves_system(self):
        is_sol_list = []
        tols_list = []
        
        tol = 1e-10
        
        for root in self.roots:
            e = EqmFinder(self.params, root)
            eqm_vec = [e.S, e.I, e.X, e.Z]

            o = ODESystem(self.params)
            derivs = o.system(0, eqm_vec)

            is_solution = all([abs(d)<tol for d in derivs])
            max_tol = max([abs(d) for d in derivs])

            is_sol_list.append(is_solution)
            tols_list.append(max_tol)

        self.roots_solve_system = is_sol_list
        self.root_sol_tol = tols_list



    def find_equilibria(self):
        S_list = []
        I_list = []
        X_list = []
        Z_list = []
        
        for root in self.roots:
            e = EqmFinder(self.params, root)
            
            S_list.append(e.S)
            I_list.append(e.I)
            X_list.append(e.X)
            Z_list.append(e.Z)

        self.S_list = S_list
        self.I_list = I_list
        self.X_list = X_list
        self.Z_list = Z_list


    def check_stability(self):
        out = []

        for ii in range(len(self.roots)):
            S = self.S_list[ii]
            I = self.I_list[ii]
            X = self.X_list[ii]
            Z = self.Z_list[ii]


            stab = StabilityMatrix(self.params, [S, I, X, Z])
            out.append(stab.is_stable)

        self.roots_are_stable = out



    def get_df(self):
        
        out = pd.DataFrame(dict(
                    S=self.S_list,
                    I=self.I_list,
                    X=self.X_list,
                    Z=self.Z_list,
                    bio_realistic=self.roots_in_range,
                    solves_system=self.roots_solve_system,
                    tol=self.root_sol_tol,
                    is_stable=self.roots_are_stable
                    ))


        self.df = out





class StabilityMatrix:
    def __init__(self, params, eqm_vec) -> None:
        self.params = params
        self.eqm = eqm_vec

        self._generate_matrix()
        self._check_if_stable()

    def _check_if_stable(self):
        summed = sum(self.matrix)
        has_nans = np.isnan(summed)
        
        if any(has_nans):
            self.is_stable = "NA"
            return None

        e_vals = np.linalg.eig(self.matrix)[0]
        
        stable = [self._negative_real_part(e) for e in e_vals]

        self.is_stable = all(stable)


    def _negative_real_part(self, e):
        if np.iscomplex(e):
            return self._is_negative(e.real)
        else:
            return self._is_negative(e)
    
    @staticmethod
    def _is_negative(e):
        if e<0:
            return True
        else:
            return False


    def _generate_matrix(self):
        e = self.eqm
        p = self.params

        S = e[0]
        I = e[1]
        X = e[2]
        Z = e[3]
        
        posDenom = S + p.nu_p * p.eps_p * I
        negDenom = S + p.nu_m * p.eps_m * I
        
        j11 = -p.gamma * Z * p.nu_p * p.eps_p * I / (p.om_p * p.Gamma * posDenom * posDenom) - p.rho
        j12 = p.gamma * Z * S * p.nu_p * p.eps_p / (p.om_p * p.Gamma * posDenom * posDenom)
        j13 = 0
        j14 = -p.gamma * S / (p.om_p * p.Gamma * posDenom)
        
        j21 = p.gamma * Z * p.nu_p * p.eps_p * I / (p.om_p * p.Gamma * posDenom * posDenom)
        j22 = -p.gamma * Z * S * p.nu_p * p.eps_p / (p.om_p * p.Gamma * posDenom * posDenom) - (p.rho + p.mu)
        j23 = 0
        j24 = p.gamma * S / (p.om_p * p.Gamma * posDenom)
        
        j31 = p.eta * X * p.nu_m * I / (p.om_m * p.Gamma * negDenom * negDenom)
        j32 = -p.eta * X * p.nu_m * S / (p.om_m * p.Gamma * negDenom * negDenom)
        j33 = p.sigma * (1 - (X + Z)/p.zeta) - (p.sigma / p.zeta) * (X + Z) - p.eta * p.nu_m * I / (p.om_m * p.Gamma * negDenom) - p.alpha
        j34 = p.sigma * (1 - (X + Z)/p.zeta) - (p.sigma / p.zeta) * (X + Z) + p.tau
        
        j41 = -p.eta * X * p.nu_m * I / (p.om_m * p.Gamma * negDenom * negDenom)
        j42 = p.eta * X * p.nu_m * S / (p.om_m * p.Gamma * negDenom * negDenom)
        j43 = p.eta * p.nu_m * I / (p.om_m * p.Gamma * negDenom)
        j44 = -(p.tau+p.alpha)
        

        # * now the extra parts for delta > 0, beta <> 1
        phi_p = (S + p.nu_p * I)/(p.om_p * p.Gamma * (S + p.nu_p * p.eps_p * I))
        phi_m = (S + p.nu_m * I)/(p.om_m * p.Gamma * (S + p.nu_m * p.eps_m * I))
        
        # these are the extra parts on the dZ/dt equation from delta > 0
        extraJ44 = -p.alpha * p.delta * (p.Gamma * phi_p - 1)
        j44 = j44 + extraJ44
        
        extraJ41 = -p.alpha * p.delta * Z * p.nu_p * (p.eps_p - 1) * I / (p.om_p * posDenom * posDenom)
        j41 = j41 + extraJ41
        
        extraJ42 = -p.alpha * p.delta * Z * p.nu_p * (1 - p.eps_p) * S / (p.om_p * posDenom * posDenom)
        j42 = j42 + extraJ42
        
        # will be corresponding extra parts on the dX/dt equation from delta > 0
        extraJ33 = -p.alpha * p.delta * (p.Gamma * phi_m - 1)
        j33 = j33 + extraJ33
        
        extraJ31 = -p.alpha * p.delta * X * p.nu_m * (p.eps_m - 1) * I / (p.om_m * negDenom * negDenom)
        j31 = j31 + extraJ31
        
        extraJ32 = -p.alpha * p.delta * X * p.nu_m * (1 - p.eps_m) * S / (p.om_m * negDenom * negDenom)
        j32 = j32 + extraJ32
        
        # and then further extra parts from beta <> 1
        g1 = p.nu_m * p.eps_m * X / negDenom
        g2 = p.nu_p * p.eps_p * Z / posDenom
        g3 = I * (1 - (X + Z)/p.zeta)
        
        extraJ31 = p.sigma * (p.beta - 1) * g3 * ( -g1/negDenom - g2/posDenom)
        j31 = j31 + extraJ31
        
        t1 = g3 * (-g1 * p.nu_m * p.eps_m / negDenom - g2 * p.nu_p * p.eps_p / posDenom) 
        t2 = (1 - (X + Z)/p.zeta) * (g1 + g2)  
        extraJ32 = p.sigma * (p.beta - 1) * (t1 + t2) 
        j32 = j32 + extraJ32
        
        t1 = g3 * (p.nu_m * p.eps_m / negDenom)
        t2 = -I / p.zeta * (g1 + g2)
        extraJ33 = p.sigma * (p.beta - 1) * (t1 + t2) 
        j33 = j33 + extraJ33
        
        t1 = g3 * (p.nu_p * p.eps_p / posDenom)
        t2 = -I / p.zeta * (g1 + g2)
        extraJ34 = p.sigma * (p.beta - 1) * (t1 + t2) 
        j34 = j34 + extraJ34
        
        J = np.array([[j11,j12,j13,j14],[j21,j22,j23,j24],[j31,j32,j33,j34],[j41,j42,j43,j44]])
        
        self.matrix = J
        


