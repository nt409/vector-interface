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

        n0_df_nN = df_non_0[~df_non_0["stab"].isin([None])]

        gap_fillers = [NonZeroGapFiller(n0_df_nN).data,
                        JoinGapFiller(n0_df_nN, self.x_info).data]

        df_n_0_s, df_n_0_u = self.incorporate_gap_fillers(gap_fillers, df_non_0)
        
        xs_plot = self.get_output_list("x", dis_free, dis_free_no_vec, df_n_0_s, df_n_0_u)
        host_plot = self.get_output_list("host", dis_free, dis_free_no_vec, df_n_0_s, df_n_0_u)
        stabs_plot = self.get_stab_output_list()

        return dict(xs=xs_plot,
                    host_vals=host_plot,
                    stabs=stabs_plot)
    


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
        
        hf_s = self.sort_dfs_by_host_first(df_s)
        hf_u = self.sort_dfs_by_host_first(df_u)

        for gap_flr in gap_fillers:
            df_s = df_s.append(gap_flr["stable"], ignore_index=True)
            df_u = df_u.append(gap_flr["unstable"], ignore_index=True)

        df_s_out = self.get_sorted_df(df_s, hf_s)
        df_u_out = self.get_sorted_df(df_u, hf_u)

        return df_s_out, df_u_out



    def sort_dfs_by_host_first(self, df):
        by_h = df.sort_values(by=["host", "x"])

        if not by_h.shape[0]:
            return True
        
        if not self.big_x_jumps(list(by_h.x)):
            return True
        else:
            return False


    @staticmethod
    def big_x_jumps(x):
        # x was linspaced, so can just check if all jumps same size

        diffs = [abs(x[ii+1] - x[ii]) for ii in range(len(x)-1)]

        if min(diffs)!=max(diffs):
            return True
        else:
            return False
    
    
    @staticmethod
    def get_sorted_df(df, host_first):

        if host_first:
            return df.sort_values(by=["host", "x"])
        else:
            return df.sort_values(by=["x", "host"])


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





def get_empty_gap_fill_dict():
    return dict(stable=pd.DataFrame(dict(x=[], host=[], stab=[])),
                    unstable=pd.DataFrame(dict(x=[], host=[], stab=[])))


def get_dict_of_dfs(xs, ys, stabs):

    if len(stabs)>2:
        print("list shouldn't be this longer than 2?")
    
    out = get_empty_gap_fill_dict()

    for x, y, stab in zip(xs, ys, stabs):
        if not x:
            continue

        if stab:
            out["stable"] = pd.DataFrame(dict(x=x, host=y, stab=stab))
        elif not stab:
            out["unstable"] = pd.DataFrame(dict(x=x, host=y, stab=stab))
    
    return out





class JoinGapFiller:
    def __init__(self, df, x_info) -> None:
        self.df = df
        self.x_info = x_info
        # dictionary containing single df (ordered by stability)
        self.data = self.connect_x_axis_to_not(df)
    

    def connect_x_axis_to_not(self, df_in):
        df = df_in.sort_values(by=["host", "x"])

        y = np.asarray(df["host"])

        if any(np.iscomplex(y)):
            return get_empty_gap_fill_dict()

        y = np.asarray(y)

        y = y.real

        close_enough = self.eqm_close_enough_to_0(y)
        
        if not close_enough:
            return get_empty_gap_fill_dict()


        x = list(df.x)
        stab = list(df.stab)


        x_join = self.get_x_vals(x, y)
        host_join = [0, y[0]]
        stability = stab[0]


        if df.shape[0]>=2:
            x_join.append(x[1])
            host_join.append(y[1])
            stability = stab[1]

        # this dict will only contain one df
        out = get_dict_of_dfs([x_join], [host_join], [stability])
        return out
        

    def get_x_vals(self, x, y):

        if len(x)>=2:
            try:
                m = (y[1] - y[0])/(x[1] - x[0])
                c = y[0] - m*x[0]
                x_linear = -c/m

                if x_linear<self.x_info["max"] and x_linear>self.x_info["min"]:
                    x0 = x_linear
                else:
                    # don't use if linear doesn't project to correct region
                    x0 = None

            except Exception as e:
                print(f"linear error: {e}")
                x0 = x[0]
        else:
            x0 = x[0]

        return [x0, x[0]]


    def eqm_close_enough_to_0(self, z):
        threshold = max(z)/15

        if min(z)>threshold:
            # if not very close to 0, then see if it is steep nearby
            # if not steep, then return False, since likely this eqm never touches 0
            
            ind = np.where(z==min(z))[0][0]

            local_threshold = max(z)/50

            # check can look both sides
            if ind==len(z) and abs(z[ind]-z[ind-1])<local_threshold:
                return False
            
            if ind==0 and abs(z[ind+1]-z[ind])<local_threshold:
                return False

            if (abs(z[ind]-z[ind-1])<local_threshold and
                        abs(z[ind+1]-z[ind])<local_threshold):
                return False
            
            return True
        
        return True
            







class NonZeroGapFiller:
    def __init__(self, df) -> None:
        self.df = df
        # dictionary containing 1 or 2 dfs (ordered by stability)
        self.data = self.connect_non_axis_points(df)
    
    
    def connect_non_axis_points(self, df_in):

        df = df_in.sort_values(by=["host", "x", "stab"])

        x = np.asarray(df.x)
        y = np.asarray(df["host"])

        if any(np.iscomplex(y)):
            return get_empty_gap_fill_dict()
        
        stop_now_x = self.jumps_are_too_big(x)
        stop_now_y = self.jumps_are_too_big(y)

        if stop_now_x or stop_now_y:
            return get_empty_gap_fill_dict()


        strd = df_in.sort_values(by=["stab", "host"])
        df_s = strd[strd.stab.isin([True])]
        df_u = strd[strd.stab.isin([False])]

        if not df_s.shape[0] or not df_u.shape[0]:
            return get_empty_gap_fill_dict()

        out = self.get_output(df_s, df_u)
        return get_dict_of_dfs(*out)


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



    
    def get_output(self, df_low, df_high):
        s_out = [True, False]

        if df_low.shape[0]>=2 and df_high.shape[0]>=2:
            # joining more points makes it look smooth

            x_out = self.get_vec_out_depth_2(df_low, df_high, "x")
            h_out = self.get_vec_out_depth_2(df_low, df_high, "host")

            return x_out, h_out, s_out
        
        else:
            x_out = self.get_vec_out_depth_1(df_low, df_high, "x")
            h_out = self.get_vec_out_depth_1(df_low, df_high, "host")

            return x_out, h_out, s_out
    

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