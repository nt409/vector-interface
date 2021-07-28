import numpy as np
import pandas as pd

from utils.fns_general import get_kappa, get_params

from model.eqm_fns import RootAnalyser, StabilityMatrix


def get_var_name_for_scan(def_or_custom, cust_choice, NPT_var, PT_var):
    if def_or_custom=="def-NPT":
        return NPT_var
    elif def_or_custom=="def-PT":
        return PT_var
    elif def_or_custom=="def-C":
        if cust_choice=="NPT":
            return NPT_var
        elif cust_choice=="PT":
            return PT_var
        else:
            raise Exception("invalid custom transmission type")
    else:
        raise Exception("invalid default vs custom choice")


def get_ps_var_info(slider_list, var):

    df = pd.DataFrame(slider_list)
    filtered = df[df["var"]==var]

    xmin = list(filtered["min"])[0]
    xmax = list(filtered["max"])[0]
    xlab = list(filtered["axis_label"])[0]
    
    xval = list(filtered["value"])[0]

    if xval>0:
        high = 100*xmax/xval
        low = 100*xmin/xval
    else:
        high = "NA"
        low = "NA"

    out = dict(min=xmin, max=xmax, value=xval, lab=xlab, high=high, low=low)

    return out





class ParScanData:
    def __init__(self, x_info, *all_params) -> None:
        
        self.var = all_params[-1]

        self.pars_use = all_params[:-1]

        self.n_points = 501

        self.x_info = x_info

        self.data = self.get_ps_data()


    def get_ps_data(self):
        
        df_non_0 = self.get_ps_equilibria_df()

        dis_free = self.get_dis_free_df()

        print(dis_free)

        gap_fillers = GapFillerTraces(dis_free, df_non_0).data
        
        xs_plot = self.get_output_list("x", gap_fillers, dis_free, df_non_0)
        host_plot = self.get_output_list("host", gap_fillers, dis_free, df_non_0)
        vec_plot = self.get_output_list("vec", gap_fillers, dis_free, df_non_0)
        stabs_plot = self.get_stab_output_list(gap_fillers)

        return dict(xs=xs_plot,
                    vec_vals=vec_plot,
                    host_vals=host_plot,
                    stabs=stabs_plot)
    
    # normal eqms
    def get_ps_equilibria_df(self):
        p = get_params(*self.pars_use)

        xs = []
        host_out = []
        vec_out = []
        stabs = []
        
        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            if self.var in ["nu", "om", "eps"]:
                setattr(p, f"{self.var}_m", x)
                setattr(p, f"{self.var}_p", x)
            else:
                setattr(p, self.var, x)

            try:
                hh, vv, stab = self.get_terminal_incidence_and_stab(p)
                host_out += hh
                vec_out += vv
                xs += [x]*len(stab)
                stabs += stab
            except Exception as e:
                print("nt error", e)

                xs += [x]
                vec_out += [None]
                host_out += [None]
                stabs += [None]
        
        return pd.DataFrame(dict(x=xs,
                                host=host_out,
                                vec=vec_out,
                                stab=stabs))


    def get_terminal_incidence_and_stab(self, p):
        df = self.get_eqm_vals(p)

        S_list = list(df.S)
        I_list = list(df.I)
        host_term_inc = [I_list[ii]/(S_list[ii] + I_list[ii])
                        for ii in range(len(S_list))]

        X_list = list(df.X)
        Z_list = list(df.Z)
        vec_term_inc = [Z_list[ii]/(X_list[ii] + Z_list[ii])
                        for ii in range(len(Z_list))]

        stability = list(df.is_stable)

        return host_term_inc, vec_term_inc, stability

    
    def get_eqm_vals(self, p):
        
        rta = RootAnalyser(p)
        
        df = rta.df

        df = df[df['bio_realistic']]

        return df

    # end of normal eqms



    # dis free eqms
    def get_dis_free_df(self):
        p = get_params(*self.pars_use)

        xs = []
        zero_inc = []
        stabs = []

        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            if self.var in ["nu", "om", "eps"]:
                setattr(p, f"{self.var}_m", x)
                setattr(p, f"{self.var}_p", x)
            else:
                setattr(p, self.var, x)
            
            kappa = get_kappa(p)
            dis_free_eqm = [p.N, 0, kappa, 0]
            stab = StabilityMatrix(p, dis_free_eqm).is_stable
            
            xs.append(x)
            zero_inc.append(0)
            stabs.append(stab)

        return pd.DataFrame(dict(x=xs, 
                        host=zero_inc,
                        vec=zero_inc,
                        stab=stabs))

    @staticmethod
    def get_output_list(key, gap_fillers, dis_free, df_non_0):
        
        dis_free_s = dis_free[dis_free["stab"].isin([True])]
        dis_free_u = dis_free[dis_free["stab"].isin([False])]
        
        df_s = df_non_0[df_non_0["stab"].isin([True, None])]
        df_u = df_non_0[df_non_0["stab"].isin([False, None])] 

        return gap_fillers[key][:-1] + [
                    list(dis_free_s[key]),
                    list(dis_free_u[key]),
                    gap_fillers[key][-1],
                    list(df_s[key]),
                    list(df_u[key])]
    
    @staticmethod
    def get_stab_output_list(gap_fillers):
        return gap_fillers["stab"][:-1] + [
                    True,
                    False,
                    gap_fillers["stab"][-1],
                    True,
                    False]









class GapFillerTraces:
    def __init__(self, dis_free_df, n0_df) -> None:
        self.dis_free_df = dis_free_df
        self.n0_df = n0_df
        self.data = self.get_data()

    
    def get_data(self):
        dis_free = self.dis_free_df
        n0_df = self.n0_df
        
        n0_df_nN = n0_df[~n0_df["stab"].isin([None])]

        xs_0, hosts_0, vecs_0, stabs_0 = self.connect_x_axis_points(dis_free)

        xs_non_0, hosts_non_0, vecs_non_0, stabs_non_0 = self.connect_non_axis_points(n0_df_nN)
        
        xs_join, hosts_join, vecs_join, stabs_join = self.connect_x_axis_to_not(n0_df_nN)

        x_out = xs_non_0 + xs_0 + xs_join
        host_out = hosts_non_0 + hosts_0 + hosts_join
        vec_out = vecs_non_0 + vecs_0 + vecs_join
        stab_out = stabs_non_0 + stabs_0 + stabs_join

        return dict(x=x_out, host=host_out, vec=vec_out, stab=stab_out)
    

    def connect_x_axis_to_not(self, n0_df_nN):
        # connect up x axis to point just above x axis
        x_join, host_join, stab_join = self.get_joiner_0_to_non_0(n0_df_nN, "host")
        _, vec_join, _ = self.get_joiner_0_to_non_0(n0_df_nN, "vec")
        return [x_join], [host_join], [vec_join], [stab_join]

    
    def connect_non_axis_points(self, n0_df_nN):
        # if no big gap, connect up all points
        xs_non_0, hosts_non_0, stabs_non_0 = self.get_joiner_non_0(n0_df_nN, "host")
        _, vecs_non_0, _ = self.get_joiner_non_0(n0_df_nN, "vec")
        return xs_non_0, hosts_non_0, vecs_non_0, stabs_non_0

    
    
    def connect_x_axis_points(self, dis_free):
        # plot all x axis points (in one colour then plot over top)
        df = dis_free.sort_values(by=["x", "stab"])

        df_s = df[df.stab.isin([True])]
        df_u = df[df.stab.isin([False])]
        
        if not df_s.shape[0] or not df_u.shape[0]:
            xs_0 = [list(df.x)]
            hosts_0 = [list(df.host)]
            vecs_0 = [list(df.vec)]
            stabs_0 = [None]
            self.x_mid = None
            return xs_0, hosts_0, vecs_0, stabs_0

        if max(list(df_s.x))<min(list(df_u.x)):
            return self.get_x_ax_output(df_s, df_u, True)

        elif max(list(df_u.x))<min(list(df_s.x)):
            return self.get_x_ax_output(df_u, df_s, False)

        else:
            xs_0 = [list(df.x)]
            hosts_0 = [list(df.host)]
            vecs_0 = [list(df.vec)]
            stabs_0 = [None]
            self.x_mid = None
            
            return xs_0, hosts_0, vecs_0, stabs_0
        

    
    
    def get_x_ax_output(self, df_low, df_high, stab):
        x_lo = max(list(df_low.x))
        x_hi = min(list(df_high.x))
        x_mid = 0.5*(x_lo+x_hi)

        x_u = [x_lo, x_mid]
        x_s = [x_mid, x_hi]

        xs_0 = [x_u, x_s]
        hosts_0 = [[0,0], [0,0]]
        vecs_0 = [[0,0], [0,0]]
        stabs_0 = [stab, not stab]

        self.x_mid = x_mid

        return xs_0, hosts_0, vecs_0, stabs_0

    
    
    def get_joiner_non_0(self, df_in, key):
        df = df_in.sort_values(by=[key, "x", "stab"])

        x = list(df.x)
        y = list(df[key])
        
        stop_now_x = self.jumps_are_too_big(x)
        stop_now_y = self.jumps_are_too_big(y)

        if stop_now_x or stop_now_y:
            return [[]], [[]], [False]

        strd = df_in.sort_values(by=["stab", key])
        df_s = strd[strd.stab.isin([True])]
        df_u = strd[strd.stab.isin([False])]

        if not df_s.shape[0] or not df_u.shape[0]:
            return [[]], [[]], [False]

        if max(df_s[key])<min(df_u[key]):
            return self.get_non_0_output(df_s, df_u, key, True)
        elif max(df_u[key])<min(df_s[key]):
            return self.get_non_0_output(df_s, df_u, key, True)
        else:
            return [x], [y], [False]

    @staticmethod
    def jumps_are_too_big(z):
        diffs = [abs(z[ii+1] - z[ii])
                        for ii in range(len(z)-1)]
        
        threshold = max(z)/20

        if max(diffs)>threshold:
            # if big jump, check whether it is just steep here
            # if not steep nearby, then don't join
            zd = np.asarray(diffs)
            ind = np.where(zd==max(diffs))[0][0]

            # check can look both sides
            if ind==len(diffs) and diffs[ind-1]<threshold:
                return True
            
            if ind==0 and diffs[ind+1]<threshold:
                return True

            if diffs[ind-1]<threshold and diffs[ind+1]<threshold:
                return True
            
            return False
        
        return False



    @staticmethod
    def get_non_0_output(df_low, df_high, key, stab):

        if df_low.shape[0]>=2 and df_high.shape[0]>=2:
            # joining more points makes it look smooth
            xL = list(df_low["x"])[1]
            xl = list(df_low["x"])[0]
            xh = list(df_high["x"])[-1]
            xH = list(df_high["x"])[-2]
            xm = 0.5*(xl + xh)


            yL = list(df_low[key])[1]
            yl = list(df_low[key])[0]
            yh = list(df_high[key])[-1]
            yH = list(df_high[key])[-2]
            ym = 0.5*(yl + yh)

            x_out = [[xL, xl, xm], [xm, xh, xH]]
            y_out = [[yL, yl, ym], [ym, yh, yH]]
            s_out = [stab, not stab]
            return x_out, y_out, s_out
        
        else:
            xl = list(df_low["x"])[0]
            xh = list(df_high["x"])[-1]
            xm = 0.5*(xl + xh)

            yl = list(df_low[key])[0]
            yh = list(df_high[key])[-1]
            ym = 0.5*(yl + yh)

            x_out = [[xl, xm], [xm, xh]]
            y_out = [[yl, ym], [ym, yh]]
            s_out = [stab, not stab]
            return x_out, y_out, s_out
            






    def get_joiner_0_to_non_0(self, df_in, key):
        df = df_in.sort_values(by=[key, "x"])

        x = list(df.x)
        stab = list(df.stab)
        y = list(df[key])

        threshold = max(y)/50

        if min(y)>threshold:
            yd = np.asarray(y)
            ind = np.where(yd==min(y))[0][0]
            
            print(abs(y[ind]-y[ind-1])<threshold,
                    abs(y[ind+1]-y[ind])<threshold)

            # check can look both sides
            if ind==len(y) and abs(y[ind]-y[ind-1])<threshold:
                return [], [], False
            
            if ind==0 and abs(y[ind+1]-y[ind])<threshold:
                return [], [], False

            if (abs(y[ind]-y[ind-1])<threshold and
                        abs(y[ind+1]-y[ind])<threshold):
                return [], [], False
        

        x1 = self.x_mid if self.x_mid is not None else x[0]
        x2 = x[0]
        
        x_join = [x1, x2]
        y_join = [0, y[0]]
        stability = stab[0]

        if df.shape[0]>=2:
            x_join.append(x[1])
            y_join.append(y[1])
            stability = stab[1]


        return x_join, y_join, stability


