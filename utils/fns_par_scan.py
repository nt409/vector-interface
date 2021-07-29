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

        data = self.get_ps_data()

        self.data = self.ensure_real(data)



    def get_ps_data(self):
        
        df_non_0 = self.get_ps_equilibria_df()

        dis_free = self.get_dis_free_df_with_vec()

        dis_free_no_vec = self.get_dis_free_df_no_vec()

        gap_fillers = GapFillerData(dis_free, df_non_0, self.x_info).data

        df_n_0_s, df_n_0_u = self.incorporate_gap_fillers(gap_fillers, df_non_0)
        
        xs_plot = self.get_output_list("x", dis_free, dis_free_no_vec, df_n_0_s, df_n_0_u)
        host_plot = self.get_output_list("host", dis_free, dis_free_no_vec, df_n_0_s, df_n_0_u)
        stabs_plot = self.get_stab_output_list()

        return dict(xs=xs_plot,
                    host_vals=host_plot,
                    stabs=stabs_plot)
    

    @staticmethod
    def ensure_real(data):
        out = {}
        for key in data.keys():
            if key=="stabs":
                out[key] = data[key]
                continue
            
            out[key] = []
            for list_ in data[key]:
                if any(np.iscomplex(list_)):
                    raise Exception(f"List should not be complex {list_}")
                else:
                    list_ = np.asarray(list_)
                    list_ = list_.real
                    out[key].append(list_)
                    
        return out


    # normal eqms
    def get_ps_equilibria_df(self):
        p = get_params(*self.pars_use)

        xs = []
        host_out = []
        stabs = []
        
        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            p = self.update_params(p, x)

            try:
                hh, stab = self.get_terminal_incidence_and_stab(p)
                host_out += hh
                xs += [x]*len(stab)
                stabs += stab
            except Exception as e:
                print("nt error", e)

                xs += [x]
                host_out += [None]
                stabs += [None]
        
        return pd.DataFrame(dict(x=xs,
                                host=host_out,
                                stab=stabs))


    def get_terminal_incidence_and_stab(self, p):
        df = self.get_eqm_vals(p)

        S_list = list(df.S)
        I_list = list(df.I)
        host_term_inc = [I_list[ii]/(S_list[ii] + I_list[ii])
                        for ii in range(len(S_list))]

        stability = list(df.is_stable)

        return host_term_inc, stability

    
    def get_eqm_vals(self, p):
        
        rta = RootAnalyser(p)
        
        df = rta.df

        df = df[df['bio_realistic']]

        return df

    # end of normal eqms



    # dis free eqms
    def get_dis_free_df_with_vec(self):
        p = get_params(*self.pars_use)

        xs = []
        zero_inc = []
        stabs = []

        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            p = self.update_params(p, x)
            
            kappa = get_kappa(p)

            dis_free_eqm = [p.N, 0, kappa, 0]
            stab = StabilityMatrix(p, dis_free_eqm).is_stable
            
            xs.append(x)
            zero_inc.append(0)
            stabs.append(stab)

        return pd.DataFrame(dict(x=xs, 
                        host=zero_inc,
                        stab=stabs))
    

    def get_dis_free_df_no_vec(self):
        p = get_params(*self.pars_use)

        xs = []
        zero_inc = []
        stabs = []

        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            p = self.update_params(p, x)
            
            dis_free_eqm = [p.N, 0, 0, 0]
            stab = StabilityMatrix(p, dis_free_eqm).is_stable
            
            xs.append(x)
            zero_inc.append(0)
            stabs.append(stab)

        return pd.DataFrame(dict(x=xs, 
                        host=zero_inc,
                        stab=stabs))

    def update_params(self, p, x):

        # the following variables have side effects:
        # - om_p if PT
        # - eps_m
        # - om_m
        
        # special cases:
        # - zeta/tau - two inputs, pick appropriate one
        # - nu - update nu_m and nu_p

        var_to_update = self.var
        
        if var_to_update=="om":
            # double update
            p.update_eta_om_m_eps_m(x, p.eps_m)
            p.update_om_p(x)
        
        elif var_to_update=="eps":
            # double update
            p.update_eta_om_m_eps_m(p.om_m, x)
            setattr(p, f"eps_p", x)
        
        elif var_to_update=="nu":
            # double update
            setattr(p, "nu_m", x)
            setattr(p, "nu_p", x)
        
        elif var_to_update=="eps_m":
            p.update_eta_om_m_eps_m(p.om_m, x)

        elif var_to_update=="om_m":
            p.update_eta_om_m_eps_m(x, p.eps_m)

        elif var_to_update=="om_p":
            p.update_om_p(x)

        elif "tau" in var_to_update:
            # so if var_to_update is tau, tau-NPT or tau-PT
            setattr(p, "tau", x)
        
        elif "zeta" in var_to_update:
            # so if var_to_update is zeta, zeta-NPT or zeta-PT
            setattr(p, "zeta", x)
        
        else:
            setattr(p, var_to_update, x)

        return p





    def incorporate_gap_fillers(self, gap_fillers, df_non_0):
        df_s = df_non_0[df_non_0["stab"].isin([True])]
        df_u = df_non_0[df_non_0["stab"].isin([False])]

        for gap_filled in ["non_0_gaps", "joiner"]:
            df_s = df_s.append(gap_fillers[gap_filled]["stable"], ignore_index=True)
            df_u = df_u.append(gap_fillers[gap_filled]["unstable"], ignore_index=True)

        df_s = df_s.sort_values(by=["host", "x"])
        df_u = df_u.sort_values(by=["host", "x"])
        
        return df_s, df_u

        

    @staticmethod
    def get_output_list(key, dis_free, dis_f_nv, df_non_0_s, df_non_0_u):
        
        dis_free_s = dis_free[dis_free["stab"].isin([True])]
        dis_free_u = dis_free[dis_free["stab"].isin([False])]
        
        dis_free_nv_s = dis_f_nv[dis_f_nv["stab"].isin([True])]
        dis_free_nv_u = dis_f_nv[dis_f_nv["stab"].isin([False])]

        return [
                list(dis_free_u[key]),
                list(dis_free_nv_u[key]),
                list(dis_free_s[key]),
                list(dis_free_nv_s[key]),
                list(df_non_0_s[key]),
                list(df_non_0_u[key]),
                ]
    
    @staticmethod
    def get_stab_output_list():
        return [
                False,
                False,
                True,
                True,
                True,
                False
                ]







class GapFillerData:
    def __init__(self, dis_free_df, n0_df, x_info) -> None:
        self.dis_free_df = dis_free_df
        self.n0_df = n0_df
        self.x_info = x_info

        self.data = self.get_data()
        


    
    def get_data(self):
        
        ds_fr = self.dis_free_df
        dis_free_nN = ds_fr[~ds_fr["stab"].isin([None])]
        _ = self.connect_x_axis_points(dis_free_nN)
        # _ = XAxisGapFiller(dis_free_nN).data

        n0_df = self.n0_df
        n0_df_nN = n0_df[~n0_df["stab"].isin([None])]

        non_0_gaps = NonZeroGapFiller(n0_df_nN).data
        
        joiner = JoinGapFiller(n0_df_nN).data

        out = {}
        
        for data, key in zip([non_0_gaps, joiner],
                             ["non_0_gaps", "joiner"]):

            df_list = self.convert_to_df(data)
            dfs_dict = self.get_stable_and_unstable_df(df_list)
            
            out[key] = {}
            if "stable" in dfs_dict.keys():
                out[key]["stable"] = dfs_dict["stable"]
            else:
                out[key]["stable"] = pd.DataFrame()

            if "unstable" in dfs_dict.keys():
                out[key]["unstable"] = dfs_dict["unstable"]
            else:
                out[key]["unstable"] = pd.DataFrame()

        return out

    
    @staticmethod
    def convert_to_df(data):
        out = []
        for ii in range(len(data["x"])):
            df = pd.DataFrame(dict(x=data["x"][ii],
                    host=data["host"][ii],
                    stab=data["stab"][ii],
                    ))
            out.append(df)
        return out


    @staticmethod
    def get_stable_and_unstable_df(df_list):

        out = {}
        for df in df_list:
            if all(df["stab"])!=all(df["stab"]):
                stabs = df["stab"]
                raise Exception(f"not all stable {stabs}")

            if all(df["stab"]):
                out["stable"] = df
            else:
                out["unstable"] = df
        return out



    
    
    def connect_x_axis_points(self, dis_free):
        
        df = dis_free.sort_values(by=["x", "stab"])

        df_s = df[df.stab.isin([True])]
        df_u = df[df.stab.isin([False])]
        
        if not df_s.shape[0] or not df_u.shape[0]:
            xs_0 = [list(df.x)]
            hosts_0 = [list(df.host)]
            stabs_0 = [None]
            self.x_mid = None
            return dict(x=xs_0, host=hosts_0, stab=stabs_0)

        if max(list(df_s.x))<min(list(df_u.x)):
            return self.get_x_ax_output(df_s, df_u, True)

        elif max(list(df_u.x))<min(list(df_s.x)):
            return self.get_x_ax_output(df_u, df_s, False)

        else:
            xs_0 = [list(df.x)]
            hosts_0 = [list(df.host)]
            stabs_0 = [None]
            self.x_mid = None
            
            return dict(x=xs_0, host=hosts_0, stab=stabs_0)
        

    
    
    def get_x_ax_output(self, df_low, df_high, stab):
        x_lo = max(list(df_low.x))
        x_hi = min(list(df_high.x))
        x_mid = 0.5*(x_lo+x_hi)

        x_u = [x_lo, x_mid]
        x_s = [x_mid, x_hi]

        xs_0 = [x_u, x_s]
        hosts_0 = [[0,0], [0,0]]
        stabs_0 = [stab, not stab]

        self.x_mid = x_mid

        return dict(x=xs_0, host=hosts_0, stab=stabs_0)

    
    




class JoinGapFiller:
    def __init__(self, df) -> None:
        self.df = df
        self.data = self.connect_x_axis_to_not(df)
    

    def connect_x_axis_to_not(self, df_in):
        df = df_in.sort_values(by=["host", "x"])

        x = list(df.x)
        stab = list(df.stab)
        y = list(df["host"])

        if any(np.iscomplex(y)):
            return [], [], False

        y = np.asarray(y)

        y = y.real

        close_enough = self.eqm_close_enough_to_0(y)
        
        if not close_enough:
            return [], [], False

        x2 = x[0]

        if df.shape[0]>=2:
            try:
                m = (y[1] - y[0])/(x[1] - x[0])
                c = y[0] - m*x[0]
                x_linear = -c/m
                if x_linear<self.x_info["max"] and x_linear>self.x_info["min"]:
                    x1 = x_linear
                else:
                    # maybe don't use if linear doesn't project to correct region??
                    x1 = x[0]
            except:
                x1 = x[0]
        else:
            x1 = x[0]

        x_join = [x1, x2]
        host_join = [0, y[0]]
        stability = stab[0]

        if df.shape[0]>=2:
            x_join.append(x[1])
            host_join.append(y[1])
            stability = stab[1]

        return dict(x=[x_join], host=[host_join], stab=[stability])
        



    def eqm_close_enough_to_0(self, z):
        threshold = max(z)/15

        if min(z)>threshold:
            
            ind = np.where(z==min(z))[0][0]

            # check can look both sides
            if ind==len(z) and abs(z[ind]-z[ind-1])<0.6*threshold:
                return False
            
            if ind==0 and abs(z[ind+1]-z[ind])<0.6*threshold:
                return False

            if (abs(z[ind]-z[ind-1])<0.6*threshold and
                        abs(z[ind+1]-z[ind])<0.6*threshold):
                return False
            
            return True
            
        else:
            return True







class NonZeroGapFiller:
    def __init__(self, df) -> None:
        self.df = df
        self.data = self.connect_non_axis_points(df)
    
    
    def connect_non_axis_points(self, df_in):

        df = df_in.sort_values(by=["host", "x", "stab"])

        x = np.asarray(df.x)
        y = np.asarray(df["host"])

        if any(np.iscomplex(y)):
            return dict(x=[[]], host=[[]], stab=[False])
        
        stop_now_x = self.jumps_are_too_big(x)
        stop_now_y = self.jumps_are_too_big(y)

        if stop_now_x or stop_now_y:
            return dict(x=[[]], host=[[]], stab=[False])


        strd = df_in.sort_values(by=["stab", "host"])
        df_s = strd[strd.stab.isin([True])]
        df_u = strd[strd.stab.isin([False])]

        if not df_s.shape[0] or not df_u.shape[0]:
            return dict(x=[[]], host=[[]], stab=[False])

        if max(df_s["host"])<min(df_u["host"]):
            return self.get_output(df_s, df_u, True)

        elif max(df_u["host"])<min(df_s["host"]):
            return self.get_output(df_u, df_s, False)

        else:
            return dict(x=[x], host=[y], stab=[False])



    @staticmethod
    def jumps_are_too_big(z):
        
        z = z.real

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



    
    def get_output(self, df_low, df_high, stab):

        if df_low.shape[0]>=2 and df_high.shape[0]>=2:
            # joining more points makes it look smooth

            x_out = self.get_vec_out_depth_2(df_low, df_high, "x")
            h_out = self.get_vec_out_depth_2(df_low, df_high, "host")
            s_out = [stab, not stab]

            return dict(x=x_out, host=h_out, stab=s_out)
        
        else:
            x_out = self.get_vec_out_depth_1(df_low, df_high, "x")
            h_out = self.get_vec_out_depth_1(df_low, df_high, "host")
            s_out = [stab, not stab]

            return dict(x=x_out, host=h_out, stab=s_out)
    

    @staticmethod
    def get_vec_out_depth_2(df_low, df_high, key):
        zL = list(df_low[key])[1]
        zl = list(df_low[key])[0]

        zh = list(df_high[key])[-1]
        zH = list(df_high[key])[-2]

        zm = 0.5*(zl + zh)

        return [[zL, zl, zm], [zm, zh, zH]]
    

    @staticmethod
    def get_vec_out_depth_1(df_low, df_high, key):
        
        zl = list(df_low[key])[0]
        zh = list(df_high[key])[-1]
        zm = 0.5*(zl + zh)

        return [[zl, zm], [zm, zh]]